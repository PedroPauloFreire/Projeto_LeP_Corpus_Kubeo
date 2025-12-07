import csv
from models import Corpus, Sentence, Word

#função para ler os dados do corpus a partir do arquivo
#path é o endereço local do arquivo com o corpus da língua Kubeo
def load_from_tsv(path):
    
    #cria nova instância da classe Corpus para armazenar os dados
    corpus = Corpus()
    
    #tenta abrir o arquivo do endereço recebido
    try:
        #codificação UTF-8 para caracteres acentuados e especiais do Kubeo
        with open(path, newline='', encoding='utf-8') as f:
            
            #lê o CSV e converte diretamente para um dicionário Python
            #dados delimitados por TAB
            reader = csv.DictReader(f, delimiter='\t')

            #variável para armazenar ID da frase corrente
            sentence_id = None
            #variável de lista para armazenar as palavras da frase corrente
            sentence_words = []


            for row in reader:

                #valida a ID de cada linha, e quando diferente da anteriro cria uma nova instância Sentence, para iniciar uma nova frase
                sid = row['sentence_id']
                if sid != sentence_id and sentence_id is not None:
                    s = Sentence(id=sentence_id, words=sentence_words)
                    corpus.add_sentence(s)
                    sentence_words = []

                #cria instância da palavra da linha atual do TSV
                w = Word.from_row(row)
                sentence_words.append(w)
                sentence_id = sid

            #adiciona a frase final que faltava
            if sentence_id is not None:
                s = Sentence(id=sentence_id, words=sentence_words)
                corpus.add_sentence(s)

    #caso não consiga abrir o arquivo no endereço indicado, retorna uma instância vazia da classe Corpus
    except FileNotFoundError:
        pass
    return corpus
