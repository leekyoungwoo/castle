import axios from 'axios';

export const version = 'v1.0.0';

export const apiUrl = '/api/v1/';
export const execUrl = '/exec/';

//요일 Array
export const dayArr = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일'];

// axios 표준 템플릿
export const requestRaw = (url, params, method, isFile) => {
  // console.log('commonFunc - requestRaw');
  params = params || {};
  const lowerMethod = method.toLowerCase();
  let dataType = 'params';

  if (lowerMethod === 'post' || lowerMethod === 'put') {
    dataType = 'data';
  }

  const axiosData = {
    method: method,
    url: url,
    [dataType]: params
  };

  if (isFile) {
    axiosData['headers'] = {
      'Content-Type': 'multipart/form-data'
    };
  }

  return axios(axiosData);
};

// API 결과 체크
export const checkAPIResult = response => {
  if (response && response.status) {
    if (response.status === 200 && response.data) {
      if (response.data.list) {
        if (Array.isArray(response.data.list)) {
          // 정상적인 결과값
          return response.data.list;
        } else {
          console.log('[cf]list가 Array가 아닙니다.');
        }
      } else if (response.data.error) {
        console.log('[cf]응답이 이상합니다. error: ' + JSON.stringify(response.data.error));
        return false;
      } else {
        console.log('[cf]data.list가 이상합니다.');
      }
    } else {
      console.log('[cf]status가 이상합니다. status: ' + response.status);
    }
  } else {
    console.log('[cf]status가 없습니다.');
  }

  return null;
};

// axios 표준 템플릿
// export const requestRaw = (url, params, method) => {
//   // console.log('commonFunc - requestRaw');
//   params = params || {};
//   const lowerMethod = method.toLowerCase();
//   let dataType = 'params';

//   if (lowerMethod === 'post' || lowerMethod === 'put') {
//     dataType = 'data';
//   }

//   return axios({
//     method: method,
//     url: url,
//     [dataType]: params
//   });
// };

// 체크박스 로직
// export const checkBoxResult = beforeValue => {
//   let afterValue;
//   // Indeterminate & 전체선택일때 -> 전체 해제
//   if (beforeValue === 1 || beforeValue === 2) {
//     afterValue = 0;
//     // 전체 선택일때는 전체 해제
//   } else {
//     afterValue = 2;
//   }

//   return afterValue;
// };

// // API Data format
// export const dataFormat = (dataList, seqType) => {
//   if (dataList && Array.isArray(dataList)) {
//     const returnData = { ordering: [], data: {} };
//     for (let i = 0, l = dataList.length; i < l; i++) {
//       const item = dataList[i];
//       const seqNo = item[seqType];
//       returnData['ordering'].push(seqNo);
//       returnData['data'][seqNo] = item;
//     }
//     return returnData;
//   }

//   return null;
// };

// // Array 2개를 합침 (기본은 중복 제거)
// export const arrayConcat = (array1, array2, noDup) => {
//   const array = array1.concat(array2);

//   if (noDup) {
//     return array;
//   } else {
//     // Array의 중복 제거 (delete Dulplicate Of Array)
//     return array.filter((item, index) => array.indexOf(item) === index);
//   }
// };

// // 외 n개 처리
// Vue.filter('textSummary', textSummary);
// export function textSummary(value, symbol, defaultText) {
//   const data = value;
//   const type = symbol ? symbol : ',';
//   let str = defaultText;

//   if (data !== null) {
//     if (data.length > 1) {
//       const array = data.split(type);
//       str = array[0] + ' 외 ' + (array.length - 1) + '개';
//     } else {
//       str = data[0];
//     }
//   }
//   return str;
// }

// const fitTwoDigit = n => {
//   return n < 10 ? '0' + n : n;
// };

// // 디바이스 정보 (userAgent에서 추출)
// export function deviceInfo(userAgent) {
//   const device = userAgent.match(new RegExp(/\((?:Linux;)?\s?(?:U;)?\s?(.*?)\)/i));
//   return device ? device[1] : '-';
// }

// // utc 시간을 epoch로 변환
// Vue.filter('epochFromDate', epochFromDate);

// export function epochFromDate(dateString) {
//   const epoch = new Date(dateString).getTime() / 1000;
//   if (isNaN(epoch)) {
//     return '-';
//   }
//   if (epoch < 0) {
//     return '-';
//   }

//   return epoch;
// }

// // epoch 시간을 utc 시간으로 변환
// Vue.filter('timeFormatFromUTCEpoch', timeFormatFromUTCEpoch);

// export function timeFormatFromUTCEpoch(epochUTC, formatType) {
//   epochUTC = Number(epochUTC);
//   if (!!!epochUTC || epochUTC === null) {
//     return '-';
//   }
//   if (typeof formatType === 'undefined') {
//     formatType = 1;
//   }

//   const d = new Date(0); // The 0 there is the key, which sets the date to the epoch
//   d.setUTCSeconds(epochUTC);

//   const yyyy = d.getFullYear();
//   const MM = d.getMonth() + 1;
//   const dd = d.getDate();
//   const hh = d.getHours();
//   const mm = d.getMinutes();
//   const ss = d.getSeconds();

//   const timeForm = fitTwoDigit(hh) + ':' + fitTwoDigit(mm);
//   let dateForm = yyyy + '-' + fitTwoDigit(MM) + '-' + fitTwoDigit(dd);
//   if (localStorage.getItem('language') === 'en') {
//     dateForm = fitTwoDigit(MM) + '/' + fitTwoDigit(dd) + '/' + yyyy;
//   }

//   if (formatType === 1) {
//     return dateForm + ' ' + timeForm + ':' + fitTwoDigit(ss);
//   } else if (formatType === 2) {
//     return dateForm + ' ' + timeForm;
//   } else if (formatType === 3) {
//     return dateForm;
//   } else if (formatType === 4) {
//     return dateForm.substr(0, 7);
//   } else if (formatType === 10) {
//     return timeForm + ':' + fitTwoDigit(ss);
//   } else {
//     //
//   }

//   return false;
// }

// //시간차이로 보기
// Vue.filter('timeDiffFromUTCEpoch', timeDiffFromUTCEpoch);

// //시간차이로 보기
// export function timeDiffFromUTCEpoch(epochUTC, type) {
//   if (epochUTC === '' || epochUTC === 0 || epochUTC === null) {
//     return '-';
//   }

//   const inputEpoch = parseInt(epochUTC) * 1000;
//   const nowEpoch = new Date().getTime();
//   let absDiff = parseInt(Math.abs(nowEpoch - inputEpoch) / 1000);
//   let diffTxt = '';
//   let diff = '';

//   // 현재 시간 기준이 아닌 소요시간
//   if (type === 2) {
//     absDiff = parseInt(Math.abs(inputEpoch) / 1000);
//   } else {
//     // 현재 시간 기준으로 시간 차이
//     if (nowEpoch > inputEpoch) {
//       diffTxt = ' 전';
//     } else if (nowEpoch < inputEpoch) {
//       diffTxt = ' 후';
//     } else {
//       diffTxt = '';
//     }
//   }

//   if (absDiff < 61) {
//     // 초단위 차이로 처리
//     diff = absDiff + '초' + diffTxt;
//   } else if (absDiff < 3601) {
//     // 분단위 차이
//     diff = parseInt(absDiff / 60) + '분' + diffTxt;
//   } else if (absDiff < 86401) {
//     // 시간단위 차이
//     diff = parseInt(absDiff / 3600) + '시간' + diffTxt;

//     addEventListener;
//   } else if (absDiff < 2592001) {
//     // 일단위 차이
//     diff = parseInt(absDiff / 86400) + '일' + diffTxt;
//   } else if (absDiff < 31536001) {
//     // 월단위 차이
//     diff = parseInt(absDiff / 2592000) + '개월' + diffTxt;
//   } else {
//     diff = parseInt(absDiff / 31536000) + '년' + diffTxt;
//   }

//   return diff;
// }

// // 시간 형식 변환
// export function timeFormat(times) {
//   if (times === '' || times === 0 || times === null) {
//     return '-';
//   }
//   const diff = [];

//   if (seconds !== 0) {
//     const hour = parseInt(seconds / 3600);
//     const min = parseInt((seconds % 3600) / 60);
//     const sec = seconds % 60;

//     if (hour > 0) {
//       diff.push(hour + lang['hour']);
//     }

//     if (min > 0) {
//       diff.push(min + lang['min']);
//     }

//     if (sec > 0) {
//       diff.push(sec + lang['sec']);
//     }

//     // diff = hour + lang['hour'] + ' ' + min + lang['min'] + ' ' + sec + lang['sec'];
//   }

//   return diff.join(' ');
// }

// Vue.filter('upperCase', value => {
//   value.toUpperCase;
// });

// // 작업내역 - 상태 변환
// export function jobResultFormat(value) {
//   let resultTxt = '-';

//   if (value === 1) {
//     resultTxt = '요청';
//   } else if (value === 2) {
//     resultTxt = '진행중';
//   } else if (value === 4) {
//     resultTxt = '성공';
//   } else if (value === 8) {
//     resultTxt = '실패';
//   } else if (value === 16) {
//     resultTxt = '취소';
//   }

//   return resultTxt;
// }

// // 자산-발급기기 데이터(JSON)에서 기기 정보만 가져옴
// Vue.filter('deviceInfo', value => {
//   const userMobileInfo = value;
//   let deviceInfo = '';

//   if (!!userMobileInfo && typeof userMobileInfo === 'object' && Object.keys(userMobileInfo).length > 0) {
//     deviceInfo = userMobileInfo.device + ' (' + userMobileInfo.os + ')';
//   } else {
//     deviceInfo = '-';
//   }

//   return deviceInfo;
// });

// // 디폴트 날짜 설정
// export function defaultDate(year, month, date, settedDate) {
//   let d = settedDate ? new Date(settedDate) : new Date();
//   let defaultValue = d.setFullYear(d.getFullYear() + year - (settedDate ? 1 : 0));
//   defaultValue = d.setMonth(d.getMonth() + month);
//   defaultValue = d.setDate(d.getDate() + date);

//   return defaultValue;
// }

// //핸드폰 형식 자동조정
// export function phoneMask(phone) {
//   phone = phone.replace(/[^\d]/g, '');
//   return phone.replace(/(\d{3})(\d{3,4})(\d{4})/, '$1-$2-$3');
// }

// // 숫자 포맷 (,)
// export function numberFormat(num) {
//   return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
// }
