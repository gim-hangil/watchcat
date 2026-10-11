<script setup>
import { onMounted, ref } from "vue";

const props = defineProps({
  station_id: Number,
  week: Array,
});

const emit = defineEmits(["update"]);
const station_id_model = ref(props.station_id || 0);
const week_models = [ref(0), ref(0), ref(0), ref(0), ref(0)];
week_models.forEach((model, i) => {
  model.value = props.week[i] || 0;
});
const week_ids = ref([]);
const station_ids = ref([]);

onMounted(async () => {
  await fetchWeekData();
  await fetchStationData();
});

async function fetchWeekData() {
  try {
    const res = await fetch("/api/week");
    const data = await res.json();
    week_ids.value = data;
  } catch (err) {
    console.error(err.message);
  }
}

async function fetchStationData() {
  try {
    const res = await fetch("/api/station");
    const data = await res.json();
    station_ids.value = [...data].sort((a, b) =>
      a.location.localeCompare(b.location, "ko"),
    );
  } catch (err) {
    console.error(err.message);
  }
}

function submit_week() {
  let week;
  try {
    week = JSON.parse(window.localStorage.getItem("week"));
    for (let i = 0; i < week_models.length; i++) {
      week[i] = week_models[i].value;
    }
  } catch {
    console.error(
      "Error parsing week data from localStorage. Initializing new week data.",
    );
    week = [0, 0, 0, 0, 0];
  }
  window.localStorage.setItem("week", JSON.stringify(week));
  alert("주차 데이터를 저장했습니다.");
  emit("update");
}

function reset_week() {
  window.localStorage.setItem("week", JSON.stringify([0, 0, 0, 0, 0]));
  alert("주차 데이터를 초기화했습니다.");
  emit("update");
}

function next_week() {
  let week;
  try {
    week = JSON.parse(window.localStorage.getItem("week"));
    for (let i = 0; i < week_models.length; i++) {
      week_models[i].value = week_models[i + 1].value;
      week[i] = week_models[i].value;
    }
  } catch {
    console.error(
      "Error parsing week data from localStorage. Initializing new week data.",
    );
    week = [0, 0, 0, 0, 0];
  }
  window.localStorage.setItem("week", JSON.stringify(week));
  emit("update");
}

function submit_station() {
  if (!station_id_model.value) {
    alert("장소를 선택해주세요.");
    return;
  }
  window.localStorage.setItem(
    "station_id",
    JSON.stringify(station_id_model.value),
  );
  alert("장소 데이터를 저장했습니다.");
  emit("update");
}

function reset_station() {
  window.localStorage.setItem("station", JSON.stringify(0));
  alert("장소 데이터를 초기화했습니다.");
  emit("update");
}
</script>

<template>
  <div class="ConfigPage">
    <div class="input" :key="i" v-for="(week_model, i) in week_models">
      <label :for="`week_id-${i}`"
        >{{ i === 0 ? "이번 주차" : `${i}주 뒤` }}:&nbsp;</label
      >
      <select
        :id="`week_id-${i}`"
        :value="week_models[i].value"
        @change="
          (event) => (week_models[i].value = parseInt(event.target.value))
        "
      >
        <option disabled>무슨 주차인가요?</option>
        <option v-for="week in week_ids" :key="week.id" :value="week.id">
          {{ week.label }}
        </option>
      </select>
    </div>
    <div class="input">
      <button class="submit" @click="submit_week()">저장</button>
    </div>
    <div class="input">
      <button class="next" @click="next_week()">다음주로</button>
    </div>
    <div class="input">
      <button class="reset" @click="reset_week()">초기화</button>
    </div>
    <hr />
    <div class="input">
      <label for="station_id">근무지:&nbsp;</label>
      <select id="station_id" v-model="station_id_model">
        <option disabled>어디서 근무하시나요?</option>
        <option
          v-for="station in station_ids"
          :key="station.id"
          :value="station.id"
        >
          {{ station.location }}
        </option>
      </select>
    </div>
    <div class="input">
      <button class="submit" @click="submit_station()">저장</button>
    </div>
    <div class="input">
      <button class="reset" @click="reset_station()">초기화</button>
    </div>
  </div>
</template>

<style scoped>
.input {
  display: flex;
  align-items: center;
  margin-bottom: 0.5em;
}
.input:last-child {
  margin-bottom: 1em;
}

label {
  text-align: right;
  width: 7em;
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

hr {
  margin: 1.5em 0;
}
</style>
