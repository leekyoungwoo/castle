const initialState = () => {
  return {
    data: [],
    directory: {},
  };
};

const state = initialState();

const getters = {
  "sideVar/STATE": (state) => {
    return state;
  },
  "sideVar/DATA": (state) => {
    return state.data;
  },
  "sideVar/DIRECTORY": (state) => {
    return state.directory;
  },
};

const mutations = {
  "sideVar/MU_INITIAL_STATE": (state) => {
    Object.assign(state, initialState());
  },
  "sideVar/MU_INITIAL_DATA": (state) => {
    state.data = {};
  },
  "sideVar/MU_SET_DATA": (state, data) => {
    let treeData = [];

    const test = (tree, parentNo) => {
      let childTree = [];

      tree.forEach((obj) => {
        if (parentNo == obj.parentDirectoryNo) {
          obj.children = test(tree, obj.directoryNo);
          childTree.push(obj);
        }
      });

      return childTree;
    };

    data.forEach((element) => {
      if (!element.parentDirectoryNo) {
        element.children = test(data, element.directoryNo);
        treeData.push(element);
      }
    });

    state.data = treeData;
  },
  "sideVar/MU_SET_DIRECTORY": (state, data) => {
    state.directory = data;
  },
};

const actions = {
  "sideVar/INITIAL_STATE": ({ commit }) => {
    commit("sideVar/MU_INITIAL_STATE");
  },
  "sideVar/INITIAL_DATA": ({ commit }) => {
    commit("siedeVar/MU_INITIAL_DATA");
  },
  "sideVar/SET_DATA": ({ commit }, data) => {
    commit("sideVar/MU_SET_DATA", data);
  },
  "sideVar/SET_DIRECTORY": ({ commit }, data) => {
    commit("sideVar/MU_SET_DIRECTORY", data);
  },
};

export default {
  state,
  mutations,
  actions,
  getters,
};
