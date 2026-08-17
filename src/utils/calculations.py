def parse_float_input(value_str: str) -> float:
    """Converte string formatada de percentual para float."""
    texto = value_str.replace("%", "").replace(",", ".").strip()
    if texto in ("", "-"):
        return 0.0
    return float(texto)


def calcular_sinal_mercado(vix: float, minerio: float, petroleo: float) -> float:
    """Calcula o sinal da equação de abertura: -VIX + Minério + Petróleo."""
    return -vix + minerio + petroleo


def avaliar_intensidade_mercado(sinal: float) -> dict:
    """Retorna a intensidade, direção e estratégia recomendada com base no sinal."""
    abs_sinal = abs(sinal)

    if abs_sinal < 1.5:
        intensidade = "LATERAL"
        cor = "#94A3B8"
        estrategia = "Extremidades - Compra no suporte / Venda na resistência"
    elif abs_sinal < 2.5:
        intensidade = "FRACA"
        cor = "#F59E0B"
        estrategia = "Abertura Fraca"
    elif abs_sinal < 4.5:
        intensidade = "MODERADA"
        cor = "#FB923C"
        estrategia = "Abertura Moderada"
    else:
        intensidade = "FORTE"
        cor = "#60A5FA"
        estrategia = "Abertura FORTE"

    if sinal > 0:
        direcao = "COMPRADORA ↑"
    elif sinal < 0:
        direcao = "VENDEDORA ↓"
    else:
        direcao = "LATERAL"

    return {
        "direcao": direcao,
        "intensidade": intensidade,
        "estrategia": estrategia,
        "cor": cor,
        "texto": f"{direcao} — {intensidade}\n{estrategia}",
    }