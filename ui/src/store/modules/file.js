const initialState = () => {
  return {
    data: [],
  };
};

const state = initialState();

const getters = {
  "file/STATE": (state) => {
    return state;
  },
  "file/DATA": (state) => {
    return state.data;
  },
};

const mutations = {
  "file/MU_INITIAL_STATE": (state) => {
    Object.assign(state, initialState());
  },
  "file/MU_INITIAL_DATA": (state) => {
    state.data = {};
  },
  "file/MU_SET_DATA": (state, data) => {
    state.data = data;
  },
};

const actions = {
  "file/INITIAL_STATE": ({ commit }) => {
    commit("file/MU_INITIAL_STATE");
  },
  "file/INITIAL_DATA": ({ commit }) => {
    commit("siedeVar/MU_INITIAL_DATA");
  },
  "file/SET_DATA": ({ commit }, data) => {
    commit("file/MU_SET_DATA", data);
  },
};

export default {
  state,
  mutations,
  actions,
  getters,
};
