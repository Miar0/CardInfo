
from django.http import HttpResponseRedirect
from generate_number import *
from django.views.generic import ListView, FormView,  DetailView, DeleteView, UpdateView
from core.forms import *
from core.models import Card, Purchase


# Create your views here.

class IndexView(ListView):
    template_name = 'index.html'
    model = Card
    paginate_by = 8


class CreateCardView(FormView):
    template_name = 'create_card.html'
    form_class = CardForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class GenerateCardView(FormView):
    template_name = 'generate_card.html'
    form_class = GenerateForm
    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)


class CardInfoView(DetailView):
    template_name = 'card_info.html'
    model = Card

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchases = Purchase.objects.filter(card_id=kwargs.get('object'))
        context['purchases'] = purchases
        return context

    def post(self, request, pk):
        card = Card.objects.get(id=pk)
        if card.status.lower() == 'active':
            card.status = 'inactive'
        elif card.status.lower() == 'inactive':
            card.status = 'active'

        card.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteCardView(DeleteView):
    template_name = 'delete_card.html'
    model = Card
    success_url = '/'


class EditCardView(UpdateView, FormView):
    template_name = 'edit_card.html'
    form_class = EditCardForm
    model = Card
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PurchaseView(FormView):
    template_name = 'purchase.html'
    form_class = PurchaseForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

