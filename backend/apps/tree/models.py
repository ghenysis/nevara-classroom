from django.db import models
from apps.users.models import User


# Seuils d'engagement (parrainage direct F1 / équipe F1-F3)
ENGAGEMENT_THRESHOLDS = [
    # (engagement_level, label, generations_unlocked, min_f1, min_team)
    (0, 'Base', 9, 0, 0),
    (1, 'Niveau 1', 10, 2, 10),
    (2, 'Niveau 2', 11, 4, 25),
    (3, 'Niveau 3', 12, 6, 50),
    (4, 'Niveau 4', 13, 8, 100),
    (5, 'Niveau 5', 14, 10, 200),
    (6, 'VIP', 15, 12, 500),
]


class TreeNode(models.Model):
    """
    Position structurelle dans l'arbre binaire (spillover).
    Le niveau d'engagement (Base→VIP) est calculé sur le parrainage direct,
    pas sur les descendants binaires.
    """
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='tree_node')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT, related_name='children')
    left_child = models.OneToOneField('self', null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    right_child = models.OneToOneField('self', null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    priority_rank = models.BigIntegerField(default=0)
    # Profondeur structurelle dans l'arbre (0 = racine globale)
    level = models.PositiveIntegerField(default=0)
    current_position = models.PositiveIntegerField(default=0)
    # Compteurs structurels (enfants binaires) — distincts du F1 parrainage
    direct_recruits = models.PositiveIntegerField(default=0)
    # Engagement (parrainage direct) — source de vérité pour les générations débloquées
    engagement_level = models.PositiveSmallIntegerField(default=0)  # 0=Base … 6=VIP
    generations_unlocked = models.PositiveSmallIntegerField(default=9)
    active_f1_count = models.PositiveIntegerField(default=0)
    active_team_count = models.PositiveIntegerField(default=0)
    loyalty_points = models.PositiveIntegerField(default=0)
    rewards_unlocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def engagement_label(self) -> str:
        for lvl, label, *_ in ENGAGEMENT_THRESHOLDS:
            if lvl == self.engagement_level:
                return label
        return 'Base'


class LoyaltyReward(models.Model):
    """Récompenses de fidélité par niveau d'engagement."""
    level = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    points_required = models.PositiveIntegerField(default=0)
    monetary_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['level']
