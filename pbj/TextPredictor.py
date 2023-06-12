import numpy as np
import re
from tqdm import tqdm
from transformers import BertTokenizer, TFBertForSequenceClassification  # Import TFBertForSequenceClassification
from tensorflow.keras.models import load_model

class TextPredictor:
    def __init__(self, path, model_filename, model_name):
        self.model_save_path = path + model_filename
        self.trained_model = load_model(self.model_save_path, custom_objects={'TFBertForSequenceClassification': TFBertForSequenceClassification})
        self.bert_tokenizer = BertTokenizer.from_pretrained(model_name)

    def predict_text_list(self, text_list):
        return_list = []
        pred_list = []
        sentence_list = []

        for index in tqdm(range(len(text_list))):
            text = text_list[index]
            text_test = text.replace('\'', '').replace('\"', '').replace("’", "").replace("‘", "").replace("“", "").replace("”", "").replace('\\', '')

            input_ids = []
            attention_masks = []

            bert_inp = self.bert_tokenizer.encode_plus(text_test, add_special_tokens=True, max_length=80, pad_to_max_length=True, return_attention_mask=True)
            input_ids.append(bert_inp['input_ids'])
            attention_masks.append(bert_inp['attention_mask'])

            input_ids = np.asarray(input_ids)
            attention_masks = np.array(attention_masks)

            preds = self.trained_model.predict([input_ids, attention_masks], batch_size=32)
            pred_labels = np.argmax(preds, axis=1)

            if pred_labels == 1:
                sentence_list.append(text_list[index])

            pred_list.append(preds[0][1])

        if len(sentence_list) == 0:
            return_list.append('추출된 문장이 없습니다.')
        elif len(sentence_list) <= 3:
            return_list = sentence_list
        else:
            temp_index_list = []
            for i in range(3):
                temp_index = np.argmax(pred_list)
                temp_index_list.append(temp_index)
                pred_list[temp_index] = -100

            temp_index_list.sort()
            for index in temp_index_list:
                return_list.append(text_list[index])

        return return_list

# path = '/content/drive/MyDrive/GOD(final_project)/'
# model_filename = 'models/klue_bert_base_eco_200000_3_7.h5'
# model_name = "klue/bert-base"
# text = "6골6도움 시즌 마무리…A매치+이적 시장에 집중스페인 프리메라리가 마요르카의 미드필더 이강인이 7일 대표팀 합류를 위해 인천국제공항을 통해 입국하고 있다. 올 시즌 6골과 도움 6개를 기록하며 화려하게 시즌을 마무리 한 이강인은 위르겐 클린스만 한국 축구대표팀 감독이 발표한 국가대표 명단에 올라 6월 중 두 차례 예정된 A매치(16일 페루·20일 엘살바도르)를 치를 예정이다. 2023.6.7/뉴스1 ⓒ News1 김진환 기자(인천공항=뉴스1) 김도용 기자 = 스페인 프리메라리가의 마요르카에서 최고의 시즌을 보낸 이강인(22)이 팬들의 환대를 받으며 귀국했다. 이제 이강인은 6월 A매치 2연전과 여름 이적 시장에 집중할 예정이다. 이강인은 7일 오후 분홍색 모자를 눌러쓰고 푸른색 티셔츠 등 편안한 복장을 착용하고 인천국제공항을 통해 입국했다.  이강인은 약 100명의 팬들로부터 편지와 꽃다발, 선물 등을 받으며 빠르게 입국장을 빠져나갔다. 마요르카에서 두 번째 시즌을 맞이한 이강인은 팀이 치른 38경기 중 33경기에 선발 출전하는 등 하비에르 아기레 감독에게 중용 받았다. 또 6골6도움을 작성하며 프로 데뷔 후 최다 공격 포인트를 기록했다.여기에 이강인은 한국 선수 최초로 프리메라리가에서 단일 시즌 두 자릿수 공격 포인트, 한 경기 멀티골 등을 달성하며 올 시즌을 더욱 의미있게 만들었다. 스페인 프리메라리가 마요르카의 미드필더 이강인이 7일 대표팀 합류를 위해 인천국제공항을 통해 입국하고 있다. 올 시즌 6골과 도움 6개를 기록하며 화려하게 시즌을 마무리 한 이강인은 위르겐 클린스만 한국 축구대표팀 감독이 발표한 국가대표 명단에 올라 6월 중 두 차례 예정된 A매치(16일 페루·20일 엘살바도르)를 치를 예정이다. 2023.6.7/뉴스1 ⓒ News1 김진환 기자시즌 내내 일관된 경기력을 선보인 이강인 덕분에 마요르카는 2시즌 연속 잔류에 성공했다. 이에 이강인은 시즌 베스트 11 미드필더 부문에도 이름을 올렸다. 소속팀의 꾸준한 출전은 대표팀에서도 입지를 다지는 계기가 됐다. 마요르카의 활약으로 이강인은 2022 카타르 월드컵 최종 명단에 승선했고, 가나와의 조별리그 2차전에서 조규성의 골을 어시스트하는 등 맹활약했다. 지난 3월 위르겐 클린스만 감독 체제로 펼쳐진 첫 A매치에도 소집돼 콜롬비아전에서는 교체 출전, 우루과이전에서는 풀타임을 소화하는 등 대표팀 내에서 존재감을 키웠다.  이강인은 오는 11일 팬 사인회에 참석한 뒤 다음날 부산에서 대표팀에 합류해 페루(16일‧부산), 엘살바도르(20일‧대전)와의 2연전에 대비한다. 더불어 이강인은 여름 이적 시장 기간을 통해 새로운 팀을 물색할 전망이다. 이강인은 올 시즌 활약을 통해 아틀레티코 마드리드(스페인)를 비롯해 맨체스터 유나이티드, 뉴캐슬, 브라이튼, 애스턴 빌라, 번리(이상 잉글랜드), AC밀란(이탈리아) 등의 관심을 받았다. 이강인은 이미 지난 1월 겨울 이적 시장에도 유수의 팀들에게 러브콜을 받았지만 마요르카의 반대로 이적이 무산된 바 있다.기사제공 뉴스1김도용 기자 (dyk0609@news1.kr)현장에서 작성된 기사입니다.김도용 기자구독김도용 기자의 구독을 취소하시겠습니까?구독에서 해당 기자의 기사가 제외됩니다.예아니오닫기구독자-응원수-[U20 월드컵] '이강인 왼발' 못지 않은 '이승원 오른발', 4강 이끌다'생애 첫 A대표팀 발탁' 제주 안현범 \"계속 두드리니까 문이 열렸다\"Copyright ⓒ 뉴스1. All rights reserved. 무단 전재 및 재배포 금지.기사 섹션 분류 가이드기사 섹션 분류 안내스포츠 기사 섹션(종목) 정보는 언론사 분류와 기술 기반의 자동 분류 시스템을 따르고 있습니다. 오분류에 대한 건은 네이버스포츠로 제보 부탁드립니다.오분류 제보하기가이드 닫기네이버에서 [뉴스1]을 구독하세요세상에 이런 일이…[사건의 재구성]"
# text_list = re.split(r'\.[^0-9]',text)

# predictor = TextPredictor(path, model_filename, model_name)
# predictions = predictor.predict_text_list(text_list)

# print(predictions)