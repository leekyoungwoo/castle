// Getters
const STATE = 'login/STATE';
const DATA = 'login/DATA';
const LOADING = 'login/LOADING';
const DEVICE = 'login/DEVICE';
const LOGIN_RESULT = 'login/LOGIN_RESULT';

// Mutations
const MU_INITIAL_STATE = 'login/MU_INITIAL_STATE';
const MU_INITIAL_FIND_USER = 'login/MU_INITIAL_FIND_USER';
const MU_SET_DATA = 'login/MU_SET_DATA';
const MU_SET_LOADING = 'login/MU_SET_LOADING';
const MU_SET_FIND_USER = 'login/MU_SET_FIND_USER';
const MU_SET_SAVE_USER = 'login/MU_SET_SAVE_USER';
const MU_SET_DEVICE = 'login/MU_SET_DEVICE';

// Actions
const INITIAL_STATE = 'login/INITIAL_STATE';
const INITIAL_FIND_USER = 'login/INITIAL_FIND_USER';
const SET_DATA = 'login/SET_DATA';
const SET_LOADING = 'login/SET_LOADING';
const SET_SAVE_USER = 'login/SET_SAVE_USER';
const SET_FIND_USER = 'login/SET_FIND_USER';
const SET_DEVICE = 'login/SET_DEVICE';

const initialState = () => {
  return {
    data: {},
    error: '',
    saveID: '',
    loading: false,
    device: null,
    loginResult: 0,
    findData: {}
  };
};

const state = initialState();

const getters = {
  [STATE]: state => {
    return state;
  },
  [DATA]: state => {
    return state.data;
  },
  [LOADING]: state => {
    return state.loading;
  },
  [DEVICE]: state => {
    return state.device;
  },
  [LOGIN_RESULT]: state => {
    return state.loginResult;
  }
};

const mutations = {
  [MU_INITIAL_STATE]: state => {
    Object.assign(state, initialState());
  },
  [MU_INITIAL_FIND_USER]: state => {
    state.findData = [];
  },
  [MU_SET_DATA]: (state, payload) => {
    // 로그인 성공
    if (payload.loginResult === 1) {
      state.data = payload.userData;
      state.error = '';

      // 아이디 / 비밀번호 실패
    } else if (payload.loginResult === 4) {
      state.error = payload.loginMessage;
    }
  },
  [MU_SET_FIND_USER]: (state, payload) => {
    state.findData = payload;
    state.error = '';
  },
  [MU_SET_LOADING]: (state, loading) => {
    state.loading = loading;
  },
  [MU_SET_SAVE_USER]: (state, payload) => {
    state.saveID = payload;
  },
  [MU_SET_DEVICE]: (state, device) => {
    state.device = device;
  }
};

const actions = {
  [INITIAL_STATE]: ({ commit }) => {
    try {
      commit(MU_INITIAL_STATE);
    } catch (ex) {
      commit(MU_INITIAL_STATE);
      console.log('action error - INITIAL_STATE');
      return;
    }
  },
  [INITIAL_FIND_USER]: ({ commit }) => {
    try {
      commit(MU_INITIAL_FIND_USER);
    } catch (ex) {
      commit(MU_INITIAL_FIND_USER);
      console.log('action error - INITIAL_FIND_USER');
      return;
    }
  },
  [SET_DATA]: ({ commit }, data) => {
    try {
      commit(MU_SET_DATA, data);
    } catch (ex) {
      commit(MU_SET_DATA, null);
      console.log('action error - SET_DATA');
      return;
    }
  },
  [SET_FIND_USER]: ({ commit }, params) => {
    try {
      commit(MU_SET_FIND_USER, params);
    } catch (ex) {
      commit(MU_SET_FIND_USER, null);
      console.log('action error - SET_FIND_USER');
      return;
    }
  },
  [SET_SAVE_USER]: ({ commit }, user) => {
    try {
      commit(MU_SET_SAVE_USER, user);
    } catch (ex) {
      commit(MU_SET_SAVE_USER, null);
      console.log('action error - SET_SAVE_USER');
      return;
    }
  },
  [SET_LOADING]: ({ commit }, loading) => {
    try {
      commit(MU_SET_LOADING, loading);
    } catch (ex) {
      commit(MU_SET_LOADING, null);
      console.log('action error - SET_LOADING');
      return;
    }
  },
  [SET_DEVICE]: ({ commit }, device) => {
    try {
      commit(MU_SET_DEVICE, device);
    } catch (ex) {
      commit(MU_SET_DEVICE, null);
      console.log('action error - SET_DEVICE');
      return;
    }
  }
};

export default {
  state,
  mutations,
  actions,
  getters
};
