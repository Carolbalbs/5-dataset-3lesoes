# ============================================================
# separar_dataset.py
# Separa o dataset em 70% treino e 30% validacao
# ATENÇÃO: rodar ANTES do augmentation e do treinamento
# ============================================================

import os
import shutil
from sklearn.model_selection import train_test_split

# ============================================================
# CONFIGURAÇÕES
# ============================================================

ORIGINAIS_DIR   = "/home/carol/shared/rna-cnn/5-dataset-3lesoes/originais"
TREINAMENTO_DIR = "/home/carol/shared/rna-cnn/5-dataset-3lesoes/treinamento/origin-70%-4train/"
VALIDACAO_DIR   = "/home/carol/shared/rna-cnn/5-dataset-3lesoes/validacao/origin-30%-4pred/"
TEST_SIZE       = 0.3
SEED            = 42

# ============================================================


def separar_dataset(originais_dir, treinamento_dir, validacao_dir, test_size, seed):

    classes = sorted([
        d for d in os.listdir(originais_dir)
        if os.path.isdir(os.path.join(originais_dir, d))
    ])

    print('=' * 60)
    print('Separação do dataset')
    print(f'Originais:    {originais_dir}')
    print(f'Treinamento:  {treinamento_dir}')
    print(f'Validacao:    {validacao_dir}')
    print(f'Proporção:    {int((1-test_size)*100)}% treino / {int(test_size*100)}% validacao')
    print(f'Seed:         {seed}')
    print('=' * 60)

    for classe in classes:
        classe_dir = os.path.join(originais_dir, classe)

        imagens = [
            f for f in os.listdir(classe_dir)
            if os.path.isfile(os.path.join(classe_dir, f))
        ]

        imagens_treino, imagens_validacao = train_test_split(
            imagens,
            test_size=test_size,
            random_state=seed
        )

        # destinos
        destino_treino   = os.path.join(treinamento_dir, classe)
        destino_validacao = os.path.join(validacao_dir, classe)

        os.makedirs(destino_treino,    exist_ok=True)
        os.makedirs(destino_validacao, exist_ok=True)

        # copia para treinamento
        for img in imagens_treino:
            src = os.path.join(classe_dir, img)
            dst = os.path.join(destino_treino, img)
            shutil.copy(src, dst)

        # copia para validacao
        for img in imagens_validacao:
            src = os.path.join(classe_dir, img)
            dst = os.path.join(destino_validacao, img)
            shutil.copy(src, dst)

        print(f'\n{classe}')
        print(f'  Total:      {len(imagens)}')
        print(f'  Treinamento: {len(imagens_treino)}  → {destino_treino}')
        print(f'  Validacao:   {len(imagens_validacao)}  → {destino_validacao}')

    print('\n' + '=' * 60)
    print('Separação concluída.')
    print(f'Proximos passos:')
    print(f'  1. Rodar augmentation em: {treinamento_dir}')
    print(f'  2. Rodar Codigo_CNN.py com as imagens augmentadas')
    print(f'  3. Rodar Evaluate_model.py com: {validacao_dir}')
    print('=' * 60)


# ============================================================

if __name__ == "__main__":

    # Verifica se as pastas de destino já existem
    destinos = [TREINAMENTO_DIR, VALIDACAO_DIR]
    existentes = [d for d in destinos if os.path.exists(d)]

    if existentes:
        print('[AVISO] As seguintes pastas já existem:')
        for d in existentes:
            print(f'  {d}')
        print('Se continuar, imagens podem ser duplicadas.')
        resposta = input('Deseja continuar mesmo assim? (s/n): ').strip().lower()
        if resposta != 's':
            print('Operação cancelada.')
            exit()

    separar_dataset(ORIGINAIS_DIR, TREINAMENTO_DIR, VALIDACAO_DIR, TEST_SIZE, SEED)