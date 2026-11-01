from django.urls import path
from .views import (
    DepositActionView, DepositListCreateView, LedgerView, PendingDepositsView,
    PendingWithdrawalsView, WalletSummaryView, WithdrawalActionView,
    WithdrawalListView, WithdrawalView, SubscriptionTopupView,
)

urlpatterns = [
    path('summary/', WalletSummaryView.as_view()),
    path('ledger/', LedgerView.as_view()),
    path('withdraw/', WithdrawalView.as_view()),
    path('deposits/', DepositListCreateView.as_view()),
    path('withdrawals/', WithdrawalListView.as_view()),
    path('subscription/topup/', SubscriptionTopupView.as_view()),
    path('admin/deposits/pending/', PendingDepositsView.as_view()),
    path('admin/deposits/<int:pk>/action/', DepositActionView.as_view(), name='admin-deposit-action'),
    path('admin/withdrawals/pending/', PendingWithdrawalsView.as_view()),
    path('admin/withdrawals/<int:pk>/action/', WithdrawalActionView.as_view()),
]
