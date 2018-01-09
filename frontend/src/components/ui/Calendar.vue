<template>
	<div class="vue-calendar">
		<div class="datepicker" :class="{'datepicker-range':range,'datepicker__clearable':clearable&&text&&!disabled}">
			<input readonly :value="text" :class="[show ? 'focus' : '', inputClass]" :disabled="disabled" :placeholder="placeholder" :name="name" v-if="type!=='inline'"/>
			<a class="datepicker-close" @click.stop="cls"></a>
			<transition name="datepicker-anim">
				<div class="datepicker-popup clearfix" :class="[popupClass,{'datepicker-inline':type==='inline'}]" tabindex="-1" v-if="show||type==='inline'">
					<div class="calendar-list">
						<ul>
							<li>전체기간</li>
							<li>오늘</li>
							<li>어제</li>
							<li>최근 7일</li>
							<li>최근 14일</li>
							<li>최근 30일</li>
							<li>이번 주</li>
							<li>이번 달</li>
							<li>지난 달</li>
							<li>직접 설정</li>
						</ul>
					</div>
					<div class="calender-view">
						<div class="calender-inner-view clearfix">
							<template v-if="range">
								<vue-datepicker-local-calendar v-model="dates[0]" :left="true"></vue-datepicker-local-calendar>
								<vue-datepicker-local-calendar v-model="dates[1]" :right="true"></vue-datepicker-local-calendar>
							</template>
							<template v-else>
								<vue-datepicker-local-calendar v-model="dates[0]"></vue-datepicker-local-calendar>
							</template>
						</div>
					</div>
					<div class="calendar-btn">
						<button type="button">취소</button>
						<button type="button">업데이트</button>
					</div>
				</div>
			</transition>
		</div>
	</div>
</template>



<script>
	import VueDatepickerLocalCalendar from 'vue-datepicker-local/src/VueDatepickerLocalCalendar.vue'
	export default {
	  name: 'Calendar',
	  components: { VueDatepickerLocalCalendar },
	  props: {
		name: [String],
		inputClass: [String],
		popupClass: [String],
		value: [Date, Array, String],
		disabled: [Boolean],
		type: {
		  type: String,
		  default: 'normal'
		},
		rangeSeparator: {
		  type: String,
		  default: '~'
		},
		clearable: {
		  type: Boolean,
		  default: false
		},
		placeholder: [String],
		disabledDate: {
		  type: Function,
		  default: () => {
			return false
		  }
		},
		format: {
		  type: String,
		  default: 'YYYY-MM-DD'
		},
		local: {
		  type: Object,
		  default () {
			return {
			  dow: 0, // Sunday is the first day of the week
			  hourTip: 'Select Hour', // tip of select hour
			  minuteTip: 'Select Minute', // tip of select minute
			  secondTip: 'Select Second', // tip of select second
			  yearSuffix: '', // suffix of head year
			  yearSuffix: '년', // format of head
			  monthsHead: '1월_2월_3월_4월_5월_6월_7월_8월_9월_10월_11월_12월'.split('_'), // months of head
			  months: '1월_2월_3월_4월_5월_6월_7월_8월_9월_10월_11월_12월'.split('_'), // months of panel
			  weeks: '일_월_화_수_목_금_토'.split('_') // weeks
			}
		  }
		}
	  },
	  data () {
		return {
		  show: false,
		  dates: this.vi(this.value)
		}
	  },
	  computed: {
		range () {
		  return this.dates.length === 2
		},
		text () {
		  const val = this.value
		  const txt = this.dates.map(date => this.tf(date)).join(` ${this.rangeSeparator} `)
		  if (Array.isArray(val)) {
			return val.length > 1 ? txt : ''
		  } else {
			return val ? txt : ''
		  }
		}
	  },
	  watch: {
		value (val) {
		  this.dates = this.vi(this.value)
		}
	  },
	  methods: {
		cls () {
		  this.$emit('input', this.range ? [] : '')
		},
		vi (val) {
		  if (Array.isArray(val)) {
			return val.length > 1 ? val.map(item => new Date(item)) : [new Date(), new Date()]
		  } else {
			return val ? new Array(new Date(val)) : [new Date()]
		  }
		},
		ok () {
		  const $this = this
		  $this.$emit('input', Array.isArray($this.value) ? $this.dates : $this.dates[0])
		  setTimeout(() => {
			$this.show = $this.range
		  })
		},
		tf (time, format) {
		  const year = time.getFullYear()
		  const month = time.getMonth()
		  const day = time.getDate()
		  const hours24 = time.getHours()
		  const hours = hours24 % 12 === 0 ? 12 : hours24 % 12
		  const minutes = time.getMinutes()
		  const seconds = time.getSeconds()
		  const milliseconds = time.getMilliseconds()
		  const dd = t => ('0' + t).slice(-2)
		  const map = {
			YYYY: year,
			MM: dd(month + 1),
			MMM: this.local.months[month],
			MMMM: this.local.monthsHead[month],
			M: month + 1,
			DD: dd(day),
			D: day,
			HH: dd(hours24),
			H: hours24,
			hh: dd(hours),
			h: hours,
			mm: dd(minutes),
			m: minutes,
			ss: dd(seconds),
			s: seconds,
			S: milliseconds
		  }
		  return (format || this.format).replace(/Y+|M+|D+|H+|h+|m+|s+|S+/g, str => map[str])
		},
		dc (e) {
		  this.show = this.$el.contains(e.target) && !this.disabled
		}
	  },
	  mounted () {
		document.addEventListener('click', this.dc)
	  },
	  beforeDestroy () {
		document.removeEventListener('click', this.dc)
	  }
	}
</script>

<style lang="scss" scoped>
</style>



