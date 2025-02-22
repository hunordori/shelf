from django import forms

class BarcodeScanForm(forms.Form):
    barcodes = forms.CharField(widget=forms.Textarea, help_text="Scan or enter the barcodes here separated by return (Enter).")
