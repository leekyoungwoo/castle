# coding=utf-8

RULE = {
    'ALL': {
        'type': 'string'
    },
    # NEW
    'ALPHABET': r'^[a-zA-Z]+$',
    'ID': r'^[a-zA-Z0-9_\-]{5,30}$',
    'CERTCODE': r'^[a-zA-Z0-9]{8,8}$',
    'ROLLBACKCODE': r'^[\-a-zA-Z0-9]{9,9}$',
    'EMAIL': r'^(?=[A-Za-z0-9][A-Za-z0-9@._%+-]{5,253}$)[A-Za-z0-9._%+-]{1,64}@(?:[A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,63}$',
    'PHONE': r'^([0-9\s\-+]){0,20}$',
    'USER_NAME': r'^([ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9]+\s{0,1})*[ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9]+$',
    'INTEGER': r'^[0-9]*$',
}