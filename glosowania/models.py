import os
from django.db import models
import datetime
from obywatele.models import User  # Custom user model

base_dir = os.path.abspath('.')


class Decyzja(models.Model):
	autor = models.CharField(max_length=200)
	tresc = models.TextField(max_length=500, null=True, verbose_name='Treść')
	kara = models.TextField(max_length=500, null=True, verbose_name='Kara')  # Kara za nie przestrzeganie przepisu
	ile_osob_podpisalo = models.SmallIntegerField(editable=False, default=0)
	data_powstania = models.DateField(editable=False, null=True)
	data_zebrania_podpisow = models.DateField(editable=False, null=True)
	data_referendum_start = models.DateField(editable=False, null=True)
	data_referendum_stop = models.DateField(editable=False, null=True)
	data_zatwierdzenia = models.DateField(editable=False, null=True)
	data_obowiazuje_od = models.DateField(editable=False, null=True)
	za = models.SmallIntegerField(default=0, editable=False)
	przeciw = models.SmallIntegerField(default=0, editable=False)
	status = models.SmallIntegerField(default=1, editable=False)

	# 0.Propozycja, 1.Brak poparcia, 2.W kolejce, 3.Referendum, 4.Odrzucone, 5.Zatwierdzone/Vacatio Legis, 6.Obowiązuje

	# TODO: data_wejscia_w_zycie = models.DateField(editable=False, default=dzis)

	def __str__(self):
		return '%s: %s on %s' % (self.pk, self.tresc, self.status)

	class Meta:
		verbose_name_plural = "Decyzje"


class ZebranePodpisy(models.Model):
	'''Lista podpisów pod wnioskiem o referendum'''
	projekt = models.ForeignKey(Decyzja, on_delete=models.CASCADE)
	podpis_uzytkownika = models.ForeignKey(User, on_delete=models.CASCADE)  # odnotowujemy kto się podpisał

	class Meta:
		unique_together = ('projekt', 'podpis_uzytkownika')


class KtoJuzGlosowal(models.Model):
	projekt = models.ForeignKey(Decyzja, on_delete=models.CASCADE)
	ktory_uzytkownik_juz_zaglosowal = models.ForeignKey(User, on_delete=models.CASCADE)

	# odnotowujemy tylko fakt głosowania

	class Meta:
		unique_together = ('projekt', 'ktory_uzytkownik_juz_zaglosowal')


#######################################################

# TODO: To powinno być składową klasy aby dało się importować.
#	   To samo jest powtórzone w "glosowania/views/ZliczajWszystko()":
WYMAGANYCH_PODPISOW = 2  # Aby zatwierdzić wniosek o referendum
CZAS_NA_ZEBRANIE_PODPISOW = datetime.timedelta(days=30)  # 365
KOLEJKA = datetime.timedelta(days=5)  # 14 czas pomiędzy zebraniem podpisów a referendum wymagany aby móc omówić skutki
CZAS_TRWANIA_REFERENDUM = datetime.timedelta(days=2)  # 3
VACATIO_LEGIS = datetime.timedelta(days=3)  # 7
PRZEBACZENIE = datetime.timedelta(days=30)  # 365
ODNOWIENIE_KARMY = datetime.timedelta(days=30)  # 365
propozycja = 1
brak_poparcia = 2
w_kolejce = 3
referendum = 4
odrzucone = 5
zatwierdzone = 6  # Vacatio Legis
obowiazuje = 7
AKCEPTUJACY = 0.6666666666  # 0.666 = 2 osoby przy 3 członkach zatwierdzają nową osobę

######################
'''
Decyzja.objects.get(pk=2)
Decyzja.objects.get(pk=pk).autor
Decyzja.objects.filter(status=0)
Decyzja.objects.all().order_by('-data_powstania')
Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
'''


# s = Uzytkownik.objects.all()


def pokaz_flow_f():
	# webbrowser.open("https://i.imgur.com/FnVthWi.png")
	print("\nStworzenie propozycji > Zbieranie podpisów > Kolejka i Dyskusja >")
	print("> Referendum > Vacatio Legis > Przepis obowiązuje")
	print('\nIle osób potrzeba do zaakceptowania/odrzucenia użytkownika:', AKCEPTUJACY)
	input("\n\n[ENTER]")
