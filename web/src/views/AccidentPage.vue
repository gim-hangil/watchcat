<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const props = defineProps({
  station_id: Number,
  week: Array,
});
const router = useRouter();
const accident_type_id = ref(0);
const accident_types = ref([]);

onMounted(async () => {
  checkProps();
  loadAccidentTypes();
});

async function loadAccidentTypes() {
  try {
    const res = await fetch("/api/accident");
    const data = await res.json();
    accident_types.value = data;
  } catch (err) {
    console.error(err.message);
  }
}

function checkProps() {
  if (!props.station_id || !props.week[0]) {
    alert("장소와 현재 주차를 설정한 뒤 사고를 등록해주세요.");
    router.push("/");
  }
}

async function submit() {
  const body = {
    week_id: props.week[0],
    type_id: accident_type_id.value,
    timestamp: parseInt(new Date().getTime() / 1000),
    station_id: props.station_id,
  };
  console.log(body);
  const res = await fetch("/api/accident", {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (res.ok) {
    alert("사고 사례가 등록되었습니다.");
  } else {
    alert("사고 사례 등록 간 문제가 발생했습니다.");
  }
  router.push("/");
}
</script>

<template>
  <div class="AccidentPage">
    <div class="input">
      <select name="accident_type_id" v-model="accident_type_id">
        <option disabled>--</option>
        <option
          v-for="accident_type in accident_types"
          :key="accident_type.id"
          :value="accident_type.id"
        >
          {{ accident_type.label }}
        </option>
      </select>
    </div>
    <div class="input">
      <button class="submit" @click="submit()">저장</button>
    </div>
  </div>
</template>

<style scoped>
.input {
  margin-bottom: 0.3em;
}
.input:last-child {
  margin-bottom: 1em;
}

input,
button,
select {
  border: 1px solid var(--ctp-mocha-text);
  border-radius: 5px;
  background-color: var(--ctp-mocha-surface1);
  width: 100%;
  padding: 0.5em 1em;
  box-sizing: border-box;
}
input,
button,
select:focus {
  outline: none;
}

button:hover {
  cursor: pointer;
}

button.submit {
  border: none;
  background-color: var(--ctp-mocha-green);
  color: var(--ctp-mocha-base);
}

button.reset {
  border: none;
  background-color: var(--ctp-mocha-red);
  color: var(--ctp-mocha-base);
}
</style>
