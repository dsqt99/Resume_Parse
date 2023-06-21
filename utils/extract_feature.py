import pandas as pd
import json
from string import punctuation
import re
import argparse

key_exp = ['Kinh nghiệm làm việc', 
           'Kinh nghiệm', 
           'Kinh nghiệm làm việc và kỹ năng',
           'Experience',
           ]

key_obj = ['Mục tiêu nghề nghiệp và sự nghiệp',
            'Mục tiêu nghề nghiệp',
            'Mục tiêu PM',
            'Mục tiêu',
            'Objective'
            ]

key_edu = ['Trình độ học vấn và bằng cấp',
            'Trình độ học vấn',
            'Trình độ',
            'Học vấn',
            'Education'
            ]

key_skill = ['Kỹ năng và sở trường',
            'Kỹ năng',
            'Các kỹ năng',
            'Skills'
            ]

key_add = ['Địa chỉ làm việc',
            'Địa chỉ thường trú',
            'Địa chỉ liên hệ',
            'Địa chỉ',
            'Address'
            ]

key_award = ['Giải thưởng và thành tích',
            'Giải thưởng',
            'Awards'
            ]

key_cert = ['Chứng chỉ và kỹ năng',
            'Chứng chỉ',
            'Certifications'
            ]

key_hobby = ['Sở thích và tính cách',
            'Sở thích',
            'Hobbies'
            ]

key_ref = ['Người tham chiếu và thông tin thêm',
            'Người tham chiếu',
            'References'
            ]

key_act = ['Hoạt động và dự án',
            'Hoạt động',
            'Activities'
            ]

key_pro = ['Dự án đã tham gia',
            'Dự án',
            'Projects'
            ]

key_info = ['Thông tin thêm về bản thân',
            'Thông tin thêm',
            'Additional information',
            'More information'
            ]

features = {'key_exp': key_exp,
            'key_obj': key_obj,
            'key_edu': key_edu,
            'key_skill': key_skill,
            'key_add': key_add,
            'key_award': key_award,
            'key_cert': key_cert,
            'key_hobby': key_hobby,
            'key_ref': key_ref,
            'key_act': key_act,
            'key_pro': key_pro,
            'key_info': key_info
            }

map_features = {'key_exp': 'work_experience',
                'key_obj': 'career_goals',
                'key_edu': 'level_learning',
                'key_skill': 'skills',
                'key_add': 'work_addr',
                'key_award': 'prizes',
                'key_cert': 'certificates',
                'key_hobby': 'hobbies',
                'key_ref': 'reference',
                'key_act': 'activities',
                'key_pro': 'projects',
                'key_info': 'extra_info'
                }

infos = ['full_name',
        'position', 
        'tel',
        'date_of_birth',
        'email',
        'gender',
        'address',
        'work_experience', 
        'study',
        'career_goals', 
        'level_learning', 
        'skills', 
        'work_addr', 
        'prizes', 
        'certificates', 
        'hobbies', 
        'reference', 
        'activities', 
        'projects', 
        'extra_info'
    ]

def preprocess_text(text):
    text = '\n'.join([t.strip() for t in text.split('\n') if t.strip() != ''])
    return text

def check_similar_text(text1, text2):
    if min(len(text1), len(text2))/max(len(text1), len(text2)) < 0.5:
        return False
    count = 0
    text1, text2 = text1.lower(), text2.lower()
    for t1 in range(min(len(text1), len(text2))):
        if text1[t1] == text2[t1]:
            count += 1
    if count/min(len(text1), len(text2)) > 0.7:
        return True

def extract_feature_from_keys(text):
    for key in features.keys():
        for k in features[key]:
            for s in text.split('\n')[:3]:
                if check_similar_text(s, k):
                    res = text.replace(s, '')
                    res_text = '\n'.join([t.strip() for t in res.split('\n') if t.strip() != ''])
                    return map_features[key], res_text
    return 'extra_info', text

def resume_extract(texts, labels):
    result = {}
    
    for info in infos:
        result[info] = ''
    result['extra_info'] = []

    for i, text in enumerate(texts):
        text = preprocess_text(text)
        if labels[i] == 'text':
            feature, res_text = extract_feature_from_keys(text)
            if feature == 'level_learning':
                tdhv = ['Trung cấp', 'Cao đẳng', 'Đại học', 'Thạc sĩ', 'Tiến sĩ']
                for td in tdhv:
                    if td.lower() in res_text.lower():
                        result[feature] = td

                import re
                edu = []
                ed = {
                            'uni': '',
                            'specialized': '',
                            'degree': '',
                            'description': '',
                            'graduation_type': '',
                            'from': '',
                            'to': ''
                        }
                print(res_text)
                university_names, specialized, degree, description, graduation_type, dutime = [], [], [], [], [], []
                uni_pattern = r"((?:Đại học|Trường đại học|Học viện|Viện|Trung cấp|Cao đẳng).+?[.!?])"
                specialized_pattern = r"((?:Chuyên ngành|Ngành|Chuyên môn).+?[.!?])"
                dutime_pattern = r"(\d{4}\s*-\s*\d{4})|(\d{2}/\d{4}\s*-\s*\d{2}/\d{4})|(\d{4}\s*-\s*nay)|(\d{2}/\d{4}\s*-\s*nay)"
                for t in res_text.split('\n'):
                    university_matches = re.findall(uni_pattern, t)
                    if len(university_matches) > 0:
                        university_names.append(t)
                    dutime_matches = re.findall(dutime_pattern, t)
                    if len(dutime_matches) > 0:
                        dutime.append(t)
                    specialized_matches = re.findall(specialized_pattern, t)
                    if len(specialized_matches) > 0:
                        specialized.append(t)
                # if len(university_names) == len(dutime):
                # ed['uni'] = university_names[i]
                # ed['from'] = from_time
                # ed['to'] = to_time
                # edu.append(ed)
                # else:
                #     edu.append(ed)
                print(university_names)
                print(specialized)
                print(dutime)
                result['study'] = edu
            elif feature == 'work_experience':
                w_e = []
                company = {
                    'company': '',
                    'position': '',
                    'description': '',
                    'from': '',
                    'to': ''
                }
                w_e.append(company)
                result[feature] = w_e
            elif feature != 'extra_info':
                result[feature] = res_text
            else:
                result['extra_info'].append(res_text)
        else:
            result[labels[i]] = text

    result['extra_info'] = '\n'.join(result['extra_info'])
    return result