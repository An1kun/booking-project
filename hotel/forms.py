from django import forms
from .models import Room

class BookRoomForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset=Room.objects.filter(reserved=False), required=True)

    class Meta:
        model = Room
        fields = ['room']  # Включите только поле комнаты

    def __init__(self, *args, **kwargs):
        hotel = kwargs.pop('hotel')  # Получаем отель при инициализации формы
        super(BookRoomForm, self).__init__(*args, **kwargs)
        # Ограничиваем выбор только комнатами данного отеля
        self.fields['room'].queryset = Room.objects.filter(hotel=hotel, reserved=False)
