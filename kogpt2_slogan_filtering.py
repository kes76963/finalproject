from sentence_transformers import SentenceTransformer, util
import numpy as np
import requests
import json
import random

#슬로건 생성
r = requests.post(
    'https://train-8dgtlge21881yafjrqb4-gpt2-train-teachable-ainize.endpoint.ainize.ai/predictions/gpt-2-ko-small-finetune', #슬로건 , 없는 정제된 5에포크
    headers = {'Content-Type' : 'application/json'
               },
    data=json.dumps({
  "text": "리니지 rpg 게임",
  "num_samples": 100,
  "length": 20
    }))

#슬로건 추가
slogan_list = []
for slogan in r.json():
    slogan = slogan.split('\n')[0]
    slogan = slogan.split(',')[1:]
    slogan = ', '.join(slogan)
    if slogan :
      slogan_list.append(slogan)
print(len(slogan_list),'개 완료')

#문장 유사도
model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

corpus = slogan_list
corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

#비교할 슬로건 선택 => 임시로 우선 정해서 정확도 확인
queries = random.sample(slogan_list, 3)


# Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
top_k = 6
for query in queries:
    query_embedding = model.encode(query, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    cos_scores = cos_scores.cpu()

    #We use np.argpartition, to only partially sort the top_k results
    top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k] # 자신을 제외한 5개

    print("\n======================\n")
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:")

    for idx in top_results[1:top_k]:
        print(corpus[idx].strip(), "(Score: %.4f)" % (cos_scores[idx]))




# sentences = ['This framework generates embeddings for each input sentence',
#     'Sentences are passed as a list of string.',
#     'The quick brown fox jumps over the lazy dog.']
#
# embeddings = model.encode(sentences, convert_to_tensor=True)
# cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)
# print(cosine_scores)

# #문장끼리 비교
# sentence1 = "고릴라 의상을 입은 누군가가 드럼을 연주하고 있다"
# sentence2 = "그 여자가 아이를 돌본다"
# # encode sentences to get their embeddings
# embedding1 = model.encode(sentence1, convert_to_tensor=True)
# embedding2 = model.encode(sentence2, convert_to_tensor=True)
# # compute similarity scores of two embeddings
# cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
# print("Sentence 1:", sentence1)
# print("Sentence 2:", sentence2)
# print("Similarity score:", cosine_scores.item())










