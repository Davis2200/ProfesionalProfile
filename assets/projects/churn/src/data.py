import pandas as pd
import numpy as np

def generar_dataset_bancario(n_clientes=120000):
    np.random.seed(42) # Para que puedas replicar los resultados
    
    meses = ['t-5', 't-4', 't-3', 't-2', 't-1', 't']
    registros = []

    for i in range(n_clientes):
        # 1. Definimos un "Índice de Propensión" (0 a 1)
        # Esto no es el target, es qué tan 'mal' se porta el cliente.
        propension_fuga = np.random.beta(2, 5) # La mayoría son leales (sesgo a la izquierda)
        
        # 2. Saldo Base (Segmentos: Masivo, Preferente, VIP)
        saldo_base = np.random.choice([5000, 25000, 80000], p=[0.7, 0.2, 0.1])
        saldo_base += np.random.normal(0, 2000)
        
        tiene_nomina_inicial = np.random.choice([1, 0], p=[0.8, 0.2])
        
        # 3. Evolución Mensual
        for idx, mes in enumerate(meses):
            # Añadimos ruido blanco al saldo (gastos normales)
            ruido = np.random.normal(1.0, 0.05)
            
            # Si el cliente tiene alta propensión, empezamos a degradar sus datos en los últimos meses
            if propension_fuga > 0.6 and idx > 3:
                factor_degradacion = 1 - (propension_fuga * (idx/10))
                saldo_mes = saldo_base * factor_degradacion * ruido
                num_trx = np.random.randint(1, 10)
                # Probabilidad de perder la nómina si se está yendo
                nomina_mes = 0 if (np.random.rand() < propension_fuga * 0.8) else tiene_nomina_inicial
                quejas_mes = np.random.poisson(0.8)
            else:
                saldo_mes = saldo_base * ruido
                num_trx = np.random.randint(15, 40)
                nomina_mes = tiene_nomina_inicial
                quejas_mes = np.random.poisson(0.05)

            registros.append({
                'id_cliente': i,
                'mes': mes,
                'saldo_mes': max(0, round(saldo_mes, 2)),
                'num_trx': num_trx,
                'tiene_nomina': nomina_mes,
                'quejas': quejas_mes,
                # EL SECRETO: El target no es igual a la propensión. 
                # Creamos un umbral con ruido para que el modelo sufra un poco.
                'target_fuga': 1 if (propension_fuga + np.random.normal(0, 0.1) > 0.7) else 0
            })

    df = pd.DataFrame(registros)
    return df

# Ejecución y guardado
if __name__ == "__main__":
    df_banca = generar_dataset_bancario()
    df_banca.to_csv('banca_transacciones.csv', index=False)
    print(f"Dataset generado con {len(df_banca)} registros.")
    print("Distribución de Fuga:")
    print(df_banca.drop_duplicates('id_cliente')['target_fuga'].value_counts(normalize=True))