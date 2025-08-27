from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class InvoiceAddress(BaseModel):
    """
    A class representing an address in a commercial invoice.

    Attributes:
        company_name: Name of the company
        street: Street address
        city: City name
        postal_code: Postal code
        state: State or region
        country: Country name
    """

    company_name: Optional[str] = Field(description="Name of the company, e.g. BC Distribution B.V.")
    street: Optional[str] = Field(description="Street address, e.g. Pelmolenlaan 15")
    city: Optional[str] = Field(description="City name, e.g. Woerden")
    postal_code: Optional[str] = Field(description="Postal code, e.g. 3447 GW")
    state: Optional[str] = Field(description="State or region, e.g. North Holland")
    country: Optional[str] = Field(description="Country name, e.g. Netherlands")

    @staticmethod
    def example():
        """
        Creates an empty example InvoiceAddress object.

        Returns:
            InvoiceAddress: An empty InvoiceAddress object.
        """
        return InvoiceAddress(
            company_name="",
            street="",
            city="",
            postal_code="",
            state="",
            country=""
        )

    def to_dict(self):
        """
        Converts the InvoiceAddress object to a dictionary.

        Returns:
            dict: The InvoiceAddress object as a dictionary.
        """
        return {
            "company_name": self.company_name,
            "street": self.street,
            "city": self.city,
            "postal_code": self.postal_code,
            "state": self.state,
            "country": self.country,
        }


class InvoiceItem(BaseModel):
    """
    A class representing an item in a commercial invoice.

    Attributes:
        item_description: Details of the goods including product, size, and lot information
        part_number: Unique identifier for the product in the seller's catalog
        eu_hts_no: Harmonized Tariff Schedule code for customs classification
        country_of_origin: Country where the goods were manufactured
        quantity: Number of units shipped
        unit_price: Price per unit in local currency
        total_price: Total price for this item
        net_weight: Weight of goods excluding packaging
        gross_weight: Total weight including packaging
        currency: Currency code for pricing
        is_dangerous_goods: Indicates if the item is classified as dangerous goods by UN standards
        un_number: UN identification number for dangerous goods
        dangerous_goods_class: UN dangerous goods classification
    """

    item_description: Optional[str] = Field(
        description="Details of the goods including product, size, and lot information, e.g. Cleaning Solution, 6 x 450 mL, LOT: 2820"
    )
    part_number: Optional[str] = Field(
        description="Unique identifier for the product, e.g. 66039"
    )
    eu_hts_no: Optional[str] = Field(
        description="EU Harmonized Tariff Schedule code, e.g. 34029010"
    )
    country_of_origin: Optional[str] = Field(
        description="Country code where goods were manufactured, e.g. IE"
    )
    quantity: Optional[int] = Field(
        description="Number of units shipped, e.g. 1"
    )
    unit_price: Optional[float] = Field(
        description="Price per unit, e.g. 100336.00"
    )
    total_price: Optional[float] = Field(
        description="Total price for this item, e.g. 100336.00"
    )
    net_weight: Optional[float] = Field(
        description="Weight of goods excluding packaging in KG, e.g. 3.50"
    )
    gross_weight: Optional[float] = Field(
        description="Total weight including packaging in KG, e.g. 25.0"
    )
    currency: Optional[str] = Field(
        description="Currency code, e.g. KRW, USD, EUR"
    )
    is_dangerous_goods: Optional[bool] = Field(
        description=(
            "Indicates if the item is classified as dangerous goods by UN standards. "
            "First, try to determine this from extracted data (item description, part number, HTS code). "
            "If it cannot be extracted, GPT should estimate based on its internal knowledge of UN dangerous goods regulations. "
            "If there is any indication of dangerous goods, set value=True."
        )
    )
    un_number: Optional[str] = Field(
        description=(
            "UN identification number for dangerous goods, e.g. UN1203. "
            "First, try to extract it from the document (item description, part number, HTS code, or other identifiers). "
            "If it cannot be extracted, GPT should provide the most likely UN number based on its internal knowledge of UN regulations."
        )
    )
    dangerous_goods_class: Optional[str] = Field(
        description=(
            "UN dangerous goods classification, e.g. Class 3 - Flammable liquids. "
            "First, try to extract it from the document. "
            "If it cannot be extracted, GPT should infer the correct class and description based on its internal knowledge of UN standards."
        )
    )
    @staticmethod
    def example():
        """
        Creates an empty example InvoiceItem object.

        Returns:
            InvoiceItem: An empty InvoiceItem object.
        """
        return InvoiceItem(
            item_description="",
            part_number="",
            eu_hts_no="",
            country_of_origin="",
            quantity=0,
            unit_price=0.0,
            total_price=0.0,
            net_weight=0.0,
            gross_weight=0.0,
            currency="",
            is_dangerous_goods=False,
            un_number="",
            dangerous_goods_class="",
        )

    def to_dict(self):
        """
        Converts the InvoiceItem object to a dictionary.

        Returns:
            dict: The InvoiceItem object as a dictionary.
        """
        return {
            "item_description": self.item_description,
            "part_number": self.part_number,
            "eu_hts_no": self.eu_hts_no,
            "country_of_origin": self.country_of_origin,
            "quantity": self.quantity,
            "unit_price": f"{self.unit_price:.2f}" if self.unit_price is not None else None,
            "total_price": f"{self.total_price:.2f}" if self.total_price is not None else None,
            "net_weight": f"{self.net_weight:.2f}" if self.net_weight is not None else None,
            "gross_weight": f"{self.gross_weight:.2f}" if self.gross_weight is not None else None,
            "currency": self.currency,
            "is_dangerous_goods": self.is_dangerous_goods,
            "un_number": self.un_number,
            "dangerous_goods_class": self.dangerous_goods_class,
        }


class EXPDCommercialInvoice(BaseModel):
    """
    A class representing an EXPD Commercial Invoice for international shipping.

    Attributes:
        seller_exporter: Company information for the seller/exporter
        seller_exporter_vat: VAT identification number for EU tax purposes
        ship_to: Consignee or final recipient information
        invoice_number: Unique identifier for the invoice
        invoice_date: Date when the invoice was issued
        customer_number: Internal buyer reference number
        ship_to_site_number: Destination site identifier
        ship_method: Mode of transport for shipping
        terms_of_delivery: Incoterm defining delivery responsibilities
        payment_terms: Payment conditions and terms
        stop_id: Logistics reference for shipment stop
        items: List of items in the invoice
        number_of_boxes: Total number of packages
        net_value: Total value excluding additional charges
        total_value: Final invoice value including all charges
        currency: Primary currency for the invoice
        total_net_weight: Total net weight of all items
        total_gross_weight: Total gross weight of all items
    """

    seller_exporter: Optional[InvoiceAddress] = Field(
        description="Company responsible for selling and exporting the goods"
    )
    seller_exporter_vat: Optional[str] = Field(
        description="VAT identification number for EU tax purposes, e.g. NL 850641469B02"
    )
    ship_to: Optional[InvoiceAddress] = Field(
        description="Consignee or final recipient of the goods"
    )
    invoice_number: Optional[str] = Field(
        description="Unique identifier assigned to the invoice, e.g. 2431998448"
    )
    invoice_date: Optional[str] = Field(
        description="Date when the invoice was issued, e.g. 17-Jun-2025"
    )
    customer_number: Optional[str] = Field(
        description="Internal reference number for the buyer, e.g. 88682"
    )
    ship_to_site_number: Optional[str] = Field(
        description="Identifier of the destination site, e.g. 736400"
    )
    ship_method: Optional[str] = Field(
        description="Mode of transport used to ship goods, e.g. NEF-AIR"
    )
    terms_of_delivery: Optional[str] = Field(
        description="Incoterm defining delivery responsibilities, e.g. DPU (Delivered at Place Unloaded)"
    )
    payment_terms: Optional[str] = Field(
        description="Payment conditions, e.g. IMMEDIATE"
    )
    stop_id: Optional[str] = Field(
        description="Logistics reference for shipment stop, e.g. STP0107326"
    )
    items: Optional[list[InvoiceItem]] = Field(
        description="List of items included in the invoice"
    )
    number_of_boxes: Optional[int] = Field(
        description="Total number of packages in shipment, e.g. 1"
    )
    net_value: Optional[float] = Field(
        description="Value of goods excluding additional charges"
    )
    total_value: Optional[float] = Field(
        description="Final invoice value including all charges"
    )
    currency: Optional[str] = Field(
        description="Primary currency for the invoice, e.g. KRW, USD, EUR"
    )
    total_net_weight: Optional[float] = Field(
        description="Total net weight of all items in KG"
    )
    total_gross_weight: Optional[float] = Field(
        description="Total gross weight of all items in KG"
    )

    @staticmethod
    def example():
        """
        Creates an empty example EXPDCommercialInvoice object.

        Returns:
            EXPDCommercialInvoice: An empty EXPDCommercialInvoice object.
        """
        return EXPDCommercialInvoice(
            seller_exporter=InvoiceAddress.example(),
            seller_exporter_vat="",
            ship_to=InvoiceAddress.example(),
            invoice_number="",
            invoice_date=datetime.now().strftime("%d-%b-%Y"),
            customer_number="",
            ship_to_site_number="",
            ship_method="",
            terms_of_delivery="",
            payment_terms="",
            stop_id="",
            items=[InvoiceItem.example()],
            number_of_boxes=0,
            net_value=0.0,
            total_value=0.0,
            currency="",
            total_net_weight=0.0,
            total_gross_weight=0.0
        )

    @staticmethod
    def from_json(json_str: str):
        """
        Creates an EXPDCommercialInvoice object from a JSON string.

        Args:
            json_str: The JSON string representing the EXPDCommercialInvoice object.

        Returns:
            EXPDCommercialInvoice: An EXPDCommercialInvoice object.
        """
        json_content = json.loads(json_str)

        def create_invoice_address(address_data):
            if address_data is None:
                return None
            return InvoiceAddress(
                company_name=address_data.get("company_name", None),
                street=address_data.get("street", None),
                city=address_data.get("city", None),
                postal_code=address_data.get("postal_code", None),
                state=address_data.get("state", None),
                country=address_data.get("country", None),
            )

        def create_invoice_item(item_data):
            if item_data is None:
                return None
            return InvoiceItem(
                item_description=item_data.get("item_description", None),
                part_number=item_data.get("part_number", None),
                eu_hts_no=item_data.get("eu_hts_no", None),
                country_of_origin=item_data.get("country_of_origin", None),
                quantity=item_data.get("quantity", None),
                unit_price=item_data.get("unit_price", None),
                total_price=item_data.get("total_price", None),
                net_weight=item_data.get("net_weight", None),
                gross_weight=item_data.get("gross_weight", None),
                currency=item_data.get("currency", None),
                is_dangerous_goods=item_data.get("is_dangerous_goods", False),
                un_number=item_data.get("un_number", None),
                dangerous_goods_class=item_data.get("dangerous_goods_class", None),
            )

        items_list = [
            create_invoice_item(item) for item in json_content.get("items", [])
        ]

        return EXPDCommercialInvoice(
            seller_exporter=create_invoice_address(json_content.get("seller_exporter", None)),
            seller_exporter_vat=json_content.get("seller_exporter_vat", None),
            ship_to=create_invoice_address(json_content.get("ship_to", None)),
            invoice_number=json_content.get("invoice_number", None),
            invoice_date=json_content.get("invoice_date", None),
            customer_number=json_content.get("customer_number", None),
            ship_to_site_number=json_content.get("ship_to_site_number", None),
            ship_method=json_content.get("ship_method", None),
            terms_of_delivery=json_content.get("terms_of_delivery", None),
            payment_terms=json_content.get("payment_terms", None),
            stop_id=json_content.get("stop_id", None),
            items=items_list,
            number_of_boxes=json_content.get("number_of_boxes", None),
            net_value=json_content.get("net_value", None),
            total_value=json_content.get("total_value", None),
            currency=json_content.get("currency", None),
            total_net_weight=json_content.get("total_net_weight", None),
            total_gross_weight=json_content.get("total_gross_weight", None),
        )

    def to_dict(self):
        """
        Converts the EXPDCommercialInvoice object to a dictionary.

        Returns:
            dict: The EXPDCommercialInvoice object as a dictionary.
        """
        def to_list(items, expected_type):
            return [item.to_dict() for item in items if isinstance(item, expected_type)]

        items_list = to_list(self.items or [], InvoiceItem)

        return {
            "seller_exporter": self.seller_exporter.to_dict() if self.seller_exporter is not None else None,
            "seller_exporter_vat": self.seller_exporter_vat,
            "ship_to": self.ship_to.to_dict() if self.ship_to is not None else None,
            "invoice_number": self.invoice_number,
            "invoice_date": self.invoice_date,
            "customer_number": self.customer_number,
            "ship_to_site_number": self.ship_to_site_number,
            "ship_method": self.ship_method,
            "terms_of_delivery": self.terms_of_delivery,
            "payment_terms": self.payment_terms,
            "stop_id": self.stop_id,
            "items": items_list,
            "number_of_boxes": self.number_of_boxes,
            "net_value": f"{self.net_value:.2f}" if self.net_value is not None else None,
            "total_value": f"{self.total_value:.2f}" if self.total_value is not None else None,
            "currency": self.currency,
            "total_net_weight": f"{self.total_net_weight:.2f}" if self.total_net_weight is not None else None,
            "total_gross_weight": f"{self.total_gross_weight:.2f}" if self.total_gross_weight is not None else None,
        }
