"""
Kanchan Jewellers Android App
Native Android version using Kivy
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch

class JewelryCalculator:
    """Same calculation logic as Streamlit app"""
    
    @staticmethod
    def calculate_final_cost(weight, metal_type, carats=None, rate_per_gram=0, making_charges_percent=14.0):
        # Calculate base cost for given weight
        base_cost = weight * rate_per_gram
        
        # Calculate making charges with different discounts for gold and silver
        making_charges = base_cost * (making_charges_percent / 100)
        
        if metal_type == "Gold":
            discounted_making_charges = making_charges * 0.75  # 25% discount
            discount_percent = "25%"
        else:  # Silver
            discounted_making_charges = making_charges * 0.50  # 50% discount
            discount_percent = "50%"
        
        # Calculate the cost before GST
        cost_before_gst = base_cost + discounted_making_charges
        
        # Calculate GST (3% on the cost before GST)
        gst = cost_before_gst * 0.03
        
        # Calculate final cost with GST
        final_cost = cost_before_gst + gst
        
        return {
            "Weight (grams)": weight,
            "Metal Type": metal_type,
            "Rate per gram": rate_per_gram,
            "Base Cost": base_cost,
            "Making Charges": making_charges,
            "Discounted Making Charges": discounted_making_charges,
            "Discount": (making_charges - discounted_making_charges),
            "Discount Percent": discount_percent,
            "Cost Before GST": cost_before_gst,
            "GST (3%)": gst,
            "Final Cost": final_cost,
            "Carats": carats if metal_type == "Gold" else None
        }

class KanchanJewellersApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        
        screen = MDScreen()
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        header = Label(
            text='💎 Kanchan Jewellers\nShuddhata Ki Pehchan',
            font_size='24sp',
            size_hint_y=None,
            height='100dp',
            halign='center'
        )
        main_layout.add_widget(header)
        
        # Input fields
        self.weight_input = MDTextField(
            hint_text="Weight (grams)",
            helper_text="Enter jewelry weight",
            input_filter="float"
        )
        
        self.metal_spinner = Spinner(
            text='Gold',
            values=['Gold', 'Silver'],
            size_hint_y=None,
            height='48dp'
        )
        
        self.carat_spinner = Spinner(
            text='22',
            values=['18', '22', '24'],
            size_hint_y=None,
            height='48dp'
        )
        
        self.rate_input = MDTextField(
            hint_text="Rate per gram",
            helper_text="Enter current rate",
            input_filter="float"
        )
        
        self.making_charges_input = MDTextField(
            hint_text="Making Charges (%)",
            helper_text="Default: 14%",
            text="14.0",
            input_filter="float"
        )
        
        # Calculate button
        calculate_btn = MDRaisedButton(
            text="Calculate Final Cost",
            size_hint_y=None,
            height='48dp',
            on_release=self.calculate_price
        )
        
        # Result label
        self.result_label = Label(
            text='Enter details and calculate',
            font_size='16sp',
            text_size=(None, None),
            halign='left'
        )
        
        # Add widgets to layout
        main_layout.add_widget(self.weight_input)
        main_layout.add_widget(self.metal_spinner)
        main_layout.add_widget(self.carat_spinner)
        main_layout.add_widget(self.rate_input)
        main_layout.add_widget(self.making_charges_input)
        main_layout.add_widget(calculate_btn)
        main_layout.add_widget(self.result_label)
        
        screen.add_widget(main_layout)
        return screen
    
    def calculate_price(self, instance):
        try:
            weight = float(self.weight_input.text or "0")
            metal_type = self.metal_spinner.text
            carats = int(self.carat_spinner.text) if metal_type == "Gold" else None
            rate = float(self.rate_input.text or "0")
            making_charges = float(self.making_charges_input.text or "14.0")
            
            result = JewelryCalculator.calculate_final_cost(
                weight, metal_type, carats, rate, making_charges
            )
            
            result_text = f"""
Final Amount: ₹{result['Final Cost']:,.2f}

Breakdown:
• Metal: {result['Metal Type']} {f"({result['Carats']}K)" if result['Carats'] else ""}
• Weight: {result['Weight (grams)']} grams
• Rate: ₹{result['Rate per gram']:,.0f}/gram
• Base Cost: ₹{result['Base Cost']:,.2f}
• Making Charges: ₹{result['Making Charges']:,.2f}
• After Discount: ₹{result['Discounted Making Charges']:,.2f}
• GST (3%): ₹{result['GST (3%)']:,.2f}
• You Save: ₹{result['Discount']:,.2f} ({result['Discount Percent']} off)
            """
            
            self.result_label.text = result_text.strip()
            
        except ValueError:
            self.result_label.text = "Please enter valid numbers"

if __name__ == '__main__':
    KanchanJewellersApp().run()