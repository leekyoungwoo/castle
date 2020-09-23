const initialState = () => {
  return {
    data: [],
  };
};

const state = initialState();

const getters = {
  "user/STATE": (state) => {
    return state;
  },
  "user/DATA": (state) => {
    return state.data;
  },
};

const mutations = {
  "user/MU_INITIAL_STATE": (state) => {
    Object.assign(state, initialState());
  },
  "user/MU_INITIAL_DATA": (state) => {
    state.data = {};
  },
  "user/MU_SET_DATA": (state, data) => {
    state.data = data;
  },
};

const actions = {
  "user/INITIAL_STATE": ({ commit }) => {
    commit("user/MU_INITIAL_STATE");
  },
  "user/INITIAL_DATA": ({ commit }) => {
    commit("user/MU_INITIAL_DATA");
  },
  "user/SET_DATA": ({ commit }, data) => {
    commit("user/MU_SET_DATA", data);
  },
};

export default {
  state,
  mutations,
  actions,
  getters,
};
