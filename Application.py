import streamlit as st
import pandas as pd
import numpy as np
from Game import Analyzer
import torch
import torch.nn.functional as f
from transformers import BertModel, BertTokenizer
from time import sleep
import os

#forms functions

nama = st.text_input("Masukkan nama Anda:")

def formCreation():
    st.header('Gemastik Pengembangan Aplikasi Permainan')
    #languages= ( 'English', 'русский', 'العربية')
    languages= ( 'Indonesia', 'English')
    chooseform(languages)
    return

def chooseform(languages):
    languageOption = st.selectbox(
        'please select your language',
        languages)
    
    if (languageOption== 'English'):
        directory = os.getcwd()
        guessesPath= directory + "\\guesses.txt"
        englishContexto= createEnglishEnvironment()
        EnglishForm(guessesPath, englishContexto)
        return
    else:
        # Tidak ada opsi lain selain English, jadi kita tidak perlu menangani kasus lain
        pass

#Forms
def EnglishForm(guessesPath, englishContexto):
    Englishcontainer = st.container()

    guess= Englishcontainer.text_input("Please enter your guess:", "type a word")
    guess= guess.strip()

    if guess == "type a word":
        Englishcontainer.info("""**how to play:**  
        Find the secret word. You have unlimited guesses.  
        The words were sorted by an artificial intelligence algorithm according to how similar they were to the secret word.  
        After submitting a word, you will see its position. The secret word is number 1.  
        The algorithm analyzed thousands of texts. It uses the context in which words are used to calculate the similarity between them.""")

        f = open(guessesPath, "w")
        f.write("Words , Similarities \n")
        f.close() 

    else:
        englishContextoDone=False
        _ ,englishContextoSimilarity, englishContextoDone, new_target_English= checkSimilarity(guess, englishContexto)
        if type(englishContextoSimilarity) != int:
            guessWrite= guess+ " , " + str(englishContextoSimilarity*1)
    
        if not englishContextoDone:
            if englishContextoSimilarity== (-1000):
                st.write("The word "+ guess+" doesent exist")
                show(englishContextoDone, guessesPath, guessWrite=None)
            else:
                show(englishContextoDone, guessesPath, guessWrite)

            if st.button('Give Up'):
                st.write(englishContexto.giveup())            
        else:
            st.write("**Congratulations you guessed the secret word**")
            st.balloons()
            setNewTarget("English", new_target_English)
            show(englishContextoDone, guessesPath, guessWrite)
            f = open(guessesPath, "w")
            f.write("Words , Similarities \n")
            f.close() 
                
    return 

def color(x):
    cold= 0
    worm= 0.65
    hot= 0.8
    amount = x[1]

    if  amount >= cold and amount<= worm :
        return ['background-color : #e81e80']*len(x)
    elif amount> worm and amount<= hot:
        return ['background-color : #Ea7051']*len(x)
    elif amount > hot:
        return ['background-color : #73f181']*len(x)
 
    
def show(englishContextoDone, guessesPath, guessWrite):
    if guessWrite != None:

        f = open(guessesPath, "a",encoding="utf-8")
        f.write(guessWrite+ "\n")
        f.close() 

    pdguessed= pd.read_csv(guessesPath, sep=",", header=0)
    pdguessed = pdguessed.drop_duplicates()
    sortedGuesses=pdguessed.sort_values(by=[pdguessed.keys()[1]], ascending=False) 
    st.dataframe(sortedGuesses.style.apply(color, axis=1), use_container_width=True)
        

#environment functions

def setNewTarget(language, new_taregt):
    directory = os.getcwd()
    targetPath = directory +"\\"+language+"Target.txt"
    f = open(targetPath, "w",encoding="utf-8")
    f.write(new_taregt)
    f.close() 

def checkSimilarity(guess , contexto):
    contexto.act(guess)
    if torch.is_tensor(contexto.reward):
        contexto.reward = contexto.reward.item()
    return contexto.observations, contexto.reward, contexto.done, contexto.new_target

#####English########


def createEnglishEnvironment():
    bert_model_name= "bert-base-multilingual-cased"
    directory= os.getcwd()
    wordsPath= directory + "\\nouns_.txt"
    available_words=[line.strip() for line in open(wordsPath, 'r')]
    targetPath= directory + "\\EnglishTarget.txt"
    targetFile = open(targetPath, "r")
    target = targetFile.read()
    targetFile.close()
    print (target)    
    embed_calc = Analyzer(similarity_func=torch.nn.CosineSimilarity(),bert_version= bert_model_name,available_words = available_words,target= target)
    return embed_calc


####### arabic ######
def createArabicEnviroment():
    bert_model_name = 'asafaya/bert-base-arabic'
    directory = os.getcwd()
    wordsPath = directory + "\\arabic_nouns.txt"
    
    available_words=[line.strip() for line in open(wordsPath, 'r',encoding="utf8")]
    targetPath= directory + "\\ArabicTarget.txt"
    targetFile = open(targetPath, "r",encoding="utf8")
    target = targetFile.read()
    targetFile.close()
    print (target)   
    embed_calc = Analyzer(similarity_func=torch.nn.CosineSimilarity(),bert_version= bert_model_name,available_words = available_words,target= target)
    return embed_calc



####### Russian ########
def createRussianEnviroment():
    bert_model_name = 'DeepPavlov/rubert-base-cased'
    directory = os.getcwd()
    wordsPath = directory + "\\russian_nouns.txt"
    available_words=[line.strip() for line in open(wordsPath, 'r',encoding="utf8")]
    targetPath= directory + "\\RussianTarget.txt"
    targetFile = open(targetPath, "r",encoding="utf8")
    target = targetFile.read()
    targetFile.close()
    print (target)    
    embed_calc = Analyzer(similarity_func=torch.nn.CosineSimilarity(),bert_version= bert_model_name,available_words = available_words,target= target)
    return embed_calc


#main code

formCreation()