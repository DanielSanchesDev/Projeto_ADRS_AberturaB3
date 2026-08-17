import customtkinter as ctk

from gui.components import MarqueeFooter
from utils.calculations import (
    avaliar_intensidade_mercado,
    calcular_sinal_mercado,
    parse_float_input,
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CarteiraApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Minhas ADRs")
        self.geometry("420x970")
        self.resizable(False, True)
        self.configure(fg_color="#0F172A")

        self.title_label = ctk.CTkLabel(
            self,
            text="CARTEIRA DE ADRs",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#F8FAFC",
        )
        self.title_label.pack(pady=(20, 10))

        self.create_adr_section()
        self.create_equation_section()
        self.create_marquee_footer()

    def create_adr_section(self):
        frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E293B")
        frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            frame,
            text="📊 ADRs",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#F1F5F9",
        ).pack(pady=12)

        self.adr_vars = {}
        self.adr_entries = {}
        self.tickers_adrs = [
            "ABEV",
            "PBR",
            "VALE",
            "ITUB",
            "BBD",
            "BDORY",
            "BOLSY",
        ]

        for ticker in self.tickers_adrs:
            row = ctk.CTkFrame(
                frame,
                corner_radius=8,
                fg_color="#334155",
                border_width=1,
                border_color="#475569",
            )
            row.pack(fill="x", padx=15, pady=4)

            ctk.CTkLabel(
                row,
                text=ticker,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#F8FAFC",
            ).pack(side="left", padx=15, pady=6)

            var = ctk.StringVar(value="0.00")
            var.trace_add(
                "write", lambda *args, t=ticker: self.calcular_total_adrs(t)
            )

            entry = ctk.CTkEntry(
                row,
                textvariable=var,
                width=110,
                height=32,
                corner_radius=8,
                justify="center",
                fg_color="#1E293B",
                text_color="#F8FAFC",
                font=ctk.CTkFont(size=13, weight="bold"),
            )
            entry.pack(side="right", padx=10, pady=6)

            self.adr_vars[ticker] = var
            self.adr_entries[ticker] = entry

        self.total_label = ctk.CTkLabel(
            frame,
            text="TOTAL ADRs: +0.00%",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#38BDF8",
        )
        self.total_label.pack(pady=15)

    def calcular_total_adrs(self, ticker_alterado=None):
        total = 0.0

        for ticker, var in self.adr_vars.items():
            entry = self.adr_entries[ticker]
            try:
                valor = parse_float_input(var.get())
                total += valor

                if valor > 0:
                    entry.configure(fg_color="#052E16", text_color="#4ADE80")
                elif valor < 0:
                    entry.configure(fg_color="#450A0A", text_color="#FCA5A5")
                else:
                    entry.configure(fg_color="#1E293B", text_color="#F8FAFC")
            except ValueError:
                entry.configure(fg_color="#1E293B", text_color="#F8FAFC")

        if total > 0:
            cor_total = "#22C55E"
        elif total < 0:
            cor_total = "#EF4444"
        else:
            cor_total = "#38BDF8"

        self.total_label.configure(
            text=f"TOTAL ADRs: {total:+.2f}%", text_color=cor_total
        )

    def create_equation_section(self):
        frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E293B")
        frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            frame,
            text="📉 EQUAÇÃO DA ABERTURA",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F1F5F9",
        ).pack(pady=12)

        self.vix_var = ctk.StringVar(value="0.00")
        self.minerio_var = ctk.StringVar(value="0.00")
        self.petroleo_var = ctk.StringVar(value="0.00")

        inputs = [
            ("VIX (%)", self.vix_var),
            ("Minério (FEF2!)", self.minerio_var),
            ("Petróleo", self.petroleo_var),
        ]

        for nome, var in inputs:
            row = ctk.CTkFrame(
                frame,
                corner_radius=8,
                fg_color="#334155",
                border_width=1,
                border_color="#475569",
            )
            row.pack(fill="x", padx=15, pady=4)

            ctk.CTkLabel(
                row,
                text=nome,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#F8FAFC",
            ).pack(side="left", padx=15, pady=6)

            ctk.CTkEntry(
                row,
                textvariable=var,
                width=110,
                height=32,
                corner_radius=8,
                justify="center",
                fg_color="#0F172A",
                text_color="#38BDF8",
                font=ctk.CTkFont(size=13, weight="bold"),
            ).pack(side="right", padx=10, pady=6)

        self.analyze_btn = ctk.CTkButton(
            frame,
            text="🔄 Analisar Mercado",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=38,
            corner_radius=10,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            command=self.analisar_mercado,
        )
        self.analyze_btn.pack(pady=15)

        self.sinal_label = ctk.CTkLabel(
            frame,
            text="SINAL: --.--%",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#F8FAFC",
        )
        self.sinal_label.pack(pady=(0, 15))

        self.intencao_label = ctk.CTkLabel(
            frame, text="", font=ctk.CTkFont(size=15, weight="bold"), wraplength=340
        )
        self.intencao_label.pack(pady=(0, 10))

    def create_marquee_footer(self):
        text = " • BBD • BDORY • BOLSY  ⚠️ ATENÇÃO: Notícias 3 estrelas no Brasil → considerar só saldo das ADRs  |  📈 ABEV • PBR • VALE • ITUB "
        footer = MarqueeFooter(self, text=text)
        footer.pack(fill="x", side="bottom", padx=10, pady=10)

    def analisar_mercado(self):
        try:
            vix = parse_float_input(self.vix_var.get())
            minerio = parse_float_input(self.minerio_var.get())
            petroleo = parse_float_input(self.petroleo_var.get())
        except Exception:
            vix, minerio, petroleo = 0.0, 0.0, 0.0

        sinal = calcular_sinal_mercado(vix, minerio, petroleo)

        if sinal > 0:
            cor_sinal = "#22C55E"
        elif sinal < 0:
            cor_sinal = "#EF4444"
        else:
            cor_sinal = "#F8FAFC"

        self.sinal_label.configure(
            text=f"SINAL: {sinal:+.2f}%", text_color=cor_sinal
        )

        analise = avaliar_intensidade_mercado(sinal)
        self.intencao_label.configure(
            text=analise["texto"], text_color=analise["cor"]
        )