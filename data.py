import yfinance as yf

def formatar_ticker(ticker: str) -> str:
    """ Adiciona '.SA' ao ticker, se necessário. """
    ticker = ticker.strip().upper()  # Remove espaços e converte para maiúsculas
    if not ticker.endswith(".SA"):
        ticker += ".SA"
    return ticker

def obter_dados_acao(ticker_symbol: str):
    """ Obtém os dados da ação a partir do Yahoo Finance. """
    ticker_symbol = formatar_ticker(ticker_symbol)
    ticker = yf.Ticker(ticker_symbol)
    
    # Dados gerais do ativo
    info = ticker.info
    historico = ticker.history(period="1y")

    # Criar um dicionário com os principais indicadores
    indicadores = {
        "Nome": info.get("longName", "N/A"),
        "Setor": info.get("sector", "N/A"),
        "P/L": info.get("trailingPE", "N/A"),
        "P/VPA": info.get("priceToBook", "N/A"),
        "ROE (%)": info.get("returnOnEquity", "N/A"),  # 🔥 REMOVIDO x100
        "Dividend Yield (%)": info.get("dividendYield", "N/A")  # 🔥 REMOVIDO x100
    }
    
    return indicadores, historico
