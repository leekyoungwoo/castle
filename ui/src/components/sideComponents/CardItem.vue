<template>
  <a-card-grid class="card-item">
    {{ props.item.fileName }}
  </a-card-grid>
</template>
<script>
const cardItme = {
  name: "CardItem",
  props: {
    item: Object,
  },
  setup(props) {
    return {
      props,
    };
  },
};
export default cardItme;
</script>

<style lang="scss" scoped>
.card-item {
  width: 120px;
  text-align: center;
  cursor: pointer;
  // box-shadow: 0 0 0 0;
  // min-width: 400px;
}
</style>
