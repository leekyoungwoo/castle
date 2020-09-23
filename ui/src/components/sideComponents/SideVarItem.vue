<template>
  <li>
    <div class="tree">
      <div class="tree-image-name">
        <div class="tree-img" @click="toggle">
          <img src="/img/icon/arr_icon_down.png" class="icon" v-if="isOpen" />
          <img src="/img/icon/arr_icon_up.png" class="icon" v-else />
        </div>
        <div class="tree-name" :class="{ bold: isOpen }" @click="onFile">
          {{ props.item.directoryName }}
          <img class="share" src="/img/icon/share-on.png" v-if="getUserState.userType === 2 && props.item.directoryOwner != getUserState.userNo" />
        </div>
        <div class="tree-img">
          <img
            src="/img/icon/btn_field.png"
            v-if="
              !!getCuurentDirectory &&
                (getCuurentDirectory.directoryNo == props.item.directoryNo)
            "
          />
        </div>
      </div>
    </div>
    <ul v-show="isOpen" v-if="isFolder">
      <SideVarItem
        class="item"
        v-for="(child, index) in props.item.children"
        :key="index"
        :item="child"
      ></SideVarItem>
    </ul>
  </li>
</template>

<script>
import { ref, computed } from "vue";
import { useStore } from "vuex";

import { apiUrl, requestRaw, checkAPIResult } from "@/util.js";

export default {
  name: "SideVarItem",
  props: {
    item: Object,
  },
  setup(props) {
    const store = useStore();
    const isOpen = ref(false);
    const isFolder = computed(() => {
      return props.item.children && props.item.children.length;
    });
    const getCuurentDirectory = computed(() => {
      return store.getters["sideVar/DIRECTORY"];
    });
    const getUserState = computed(() => {
      return store.getters["login/DATA"];
    });

    const toggle = () => {
      isOpen.value = !isOpen.value;
    };

    const onFile = async () => {
      if (getCuurentDirectory.value.directoryNo != props.item.directoryNo) {
        const params = { directoryNo: props.item.directoryNo };
        const respObj = checkAPIResult(
          await requestRaw(apiUrl + "File", params, "get")
        );
        if (respObj) {
          store.dispatch("file/SET_DATA", respObj);
          store.dispatch("sideVar/SET_DIRECTORY", props.item);
        }
      }
    };

    return {
      isOpen,
      isFolder,
      toggle,
      props,
      onFile,
      getCuurentDirectory,
      getUserState,
    };
  },
};
</script>

<style lang="scss" scoped>
.tree {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  text-align: left;
  border-bottom: 1px solid #8178db;
  padding: 4px;
  .icon {
    margin-bottom: 2px;
  }
  .share {
    margin: 0 0 2px 5px;
  }
  .tree-image-name {
    display: flex;
    .tree-img {
      margin: 0 10px 0 5px;
    }

    .tree-name {
      flex: 1;
    }
  }
}
.item {
  cursor: pointer;
}
.bold {
  font-weight: bold;
}
ul {
  list-style: none;
  padding-left: 5px;
}
li {
  list-style: none;
}
</style>
