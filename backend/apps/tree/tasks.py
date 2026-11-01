from celery import shared_task
from django.db import transaction
from django.db.models import Count
from django.utils import timezone
from apps.users.models import User
from .models import TreeNode
from .services import repair_tree_integrity, refresh_engagement_level


@shared_task(name='apps.tree.tasks.recalculate_tree_priority')
def recalculate_tree_priority():
    """
    Cron réseau (30h) :
    1. Répare structure (profondeur / positions)
    2. Recalcule direct_recruits structurels
    3. Rafraîchit engagement_level (parrainage direct F1/équipe)
    4. Attribue priority_rank
    """
    repaired = repair_tree_integrity()

    with transaction.atomic():
        recruit_map = {
            row['parent_id']: row['c']
            for row in TreeNode.objects.filter(parent_id__isnull=False)
            .values('parent_id')
            .annotate(c=Count('id'))
        }
        for node in TreeNode.objects.select_for_update().all():
            expected = recruit_map.get(node.pk, 0)
            structural = int(bool(node.left_child_id)) + int(bool(node.right_child_id))
            expected = max(expected, structural)
            if node.direct_recruits != expected:
                TreeNode.objects.filter(pk=node.pk).update(direct_recruits=expected)

        engagement_updates = 0
        for node in TreeNode.objects.select_related('user').all():
            before = node.engagement_level
            refresh_engagement_level(node.user)
            node.refresh_from_db()
            if node.engagement_level != before:
                engagement_updates += 1

        nodes = list(TreeNode.objects.select_related('user').all())
        nodes.sort(
            key=lambda n: (
                0 if n.user.status == User.Status.ACTIVE else 1,
                n.user.current_cycle_due_date or timezone.now(),
                n.user.registration_timestamp or timezone.now(),
                str(n.user_id),
            )
        )
        for rank, node in enumerate(nodes, start=1):
            TreeNode.objects.filter(pk=node.pk).update(priority_rank=rank)

    return {
        'nodes': len(nodes),
        'repaired_positions': repaired,
        'engagement_updates': engagement_updates,
        'ran_at': timezone.now().isoformat(),
    }
