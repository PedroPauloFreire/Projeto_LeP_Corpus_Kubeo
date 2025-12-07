import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Word:
    #definir os dados da classe:
    id: str
    form: str #palavra em Kubeo como está no texto original
    lemma: Optional[str] #forma raiz da palavra, sem flexão
    pos: Optional[str] #part of speech (classe gramatical)
    glosa_ptbr: Optional[str] #tradução ou glosa em PTBR
    propriedades: Dict[str, Any] = field(default_factory=dict)
    sentence_id: str = None
    word_index: int = None #posição da palavra na frase

    #método de fábrica para converter a linha do TSV para instância de Word
    @classmethod
    def from_row(cls, row: dict):
        return cls(
            id=row.get("id") or str(uuid.uuid4()),
            form=row.get("kubeo_form"),
            lemma=row.get("lemma"),
            pos=row.get("pos"),
            glosa_ptbr=row.get("glosa_ptbr"),
            propriedades={
                #Propriedades de nomes
                "gênero": row.get("gender"),
                "número": row.get("number"),
                "contável": row.get("countable"),

                #Propriedades de verbos
                "modo": row.get("mood"),
                "tempo": row.get("tense"),
                "aspecto": row.get("aspect"),
                "pessoa verbal": row.get("person"), 
                
                "notas": row.get("notes"),      #espaço livre para anotações relevantes
            },
            sentence_id=row.get("sentence_id"),
            word_index=int(row.get("word_index")) if row.get("word_index") else None
        )

@dataclass
class Sentence:
    id: str
    #lista de palavras na frase definida como Lista de instâncias Word
    words: List[Word] = field(default_factory=list) #ajuste para usar um objeto mutável dentro do @dataclass

    def render_html(self):
        parts = []
        for w in self.words:
            parts.append(f'<span class="word" data-word-id="{w.id}">{w.form}</span>')
        return " ".join(parts)

class Corpus:
    #redifinindo o __innit__ de Corpus para incluir as propriedades 'sentences' e 'words'
    def __init__(self):
        self.sentences: Dict[str, Sentence] = {}
        self.words: Dict[str, Word] = {}

    def add_sentence(self, sentence: Sentence):
        #atribui a frase à lista na posição da ID da frase recebida como parâmetro 
        self.sentences[sentence.id] = sentence

        #para cada palavra da nova frase, adicionar a palavra à lista do Corpus
        for w in sentence.words:
            self.words[w.id] = w
