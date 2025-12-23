<template>
  <div class="nav-panel">
    <div class="pixel-panel__content">
      <div class="sprite" :style="style" />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  src: { type: String, required: true },
  frameWidth: { type: Number, required: true },   // 예: 128
  frameHeight: { type: Number, required: true },  // 예: 128
  frames: { type: Number, required: true },       // 예: 8
  fps: { type: Number, default: 8 },              // 초당 프레임
  scale: { type: Number, default: 2 },            // 픽셀 확대 배율
  row: { type: Number, default: 0 },              // 여러 행이면 row로 동작 선택
});

const style = computed(() => {
  const sheetW = props.frameWidth * props.frames;
  const sheetH = props.frameHeight; // row 여러개면 전체 높이는 이미지에 맞춰도 됨(여기선 row만 y로 이동)
  const duration = props.frames / props.fps; // 8프레임 / 8fps = 1초

  return {
    width: `${props.frameWidth}px`,
    height: `${props.frameHeight}px`,
    backgroundImage: `url(${props.src})`,
    backgroundRepeat: "no-repeat",
    backgroundSize: `${sheetW}px ${sheetH}px`,
    backgroundPosition: `0px ${-props.row * props.frameHeight}px`,
    animationDuration: `${duration}s`,
    transform: `scale(${props.scale})`,
    transformOrigin: "top left",
    "--end-x": `-${sheetW}px`,
    "--steps": props.frames,
  };
});
</script>

<style scoped>
.sprite {
  image-rendering: pixelated;
  will-change: background-position;
  animation-name: play;
  animation-timing-function: steps(var(--steps));
  animation-iteration-count: infinite;
}

@keyframes play {
  from { background-position-x: 0px; }
  to   { background-position-x: var(--end-x); }
}
</style>
