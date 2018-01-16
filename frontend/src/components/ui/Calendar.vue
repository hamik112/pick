<template>
	<div class="vue-calendar">
		<div class="datepicker" :class="{'datepicker-range':range,'datepicker__clearable':clearable&&text&&!disabled}">
			<input readonly :value="text" :class="[show ? 'focus' : '', inputClass]" :disabled="disabled" :placeholder="placeholder" :name="name" v-if="type!=='inline'"/>
			<a class="datepicker-close" href="javascript:void(0)" @click.stop="cls"></a>
			<transition name="datepicker-anim">
				<div class="datepicker-popup clearfix" :class="[popupClass,{'datepicker-inline':type==='inline'}]" tabindex="-1" v-if="show||type==='inline'">
					<div class="calendar-list">
						<ul>
							<li><a href="javascript:void(0)" @click="op('all',1)" v-bind:class="[(this.calListActive === 1) ? 'active' : '']">전체기간</a></li>
							<li><a href="javascript:void(0)" @click="op('today',2)" v-bind:class="[(this.calListActive === 2) ? 'active' : '']">오늘</a></li>
							<li><a href="javascript:void(0)" @click="op('1',3)" v-bind:class="[(this.calListActive === 3) ? 'active' : '']">어제</a></li>
							<li><a href="javascript:void(0)" @click="op('7',4)" v-bind:class="[(this.calListActive === 4) ? 'active' : '']">최근 7일</a></li>
							<li><a href="javascript:void(0)" @click="op('14',5)" v-bind:class="[(this.calListActive === 5) ? 'active' : '']">최근 14일</a></li>
							<li><a href="javascript:void(0)" @click="op('30',6)" v-bind:class="[(this.calListActive === 6) ? 'active' : '']">최근 30일</a></li>
							<li><a href="javascript:void(0)" @click="op('tWeek',7)" v-bind:class="[(this.calListActive === 7) ? 'active' : '']">이번 주</a></li>
							<li><a href="javascript:void(0)" @click="op('lWeek',8)" v-bind:class="[(this.calListActive === 8) ? 'active' : '']">지난 주</a></li>
							<li><a href="javascript:void(0)" @click="op('tMonth',9)" v-bind:class="[(this.calListActive === 9) ? 'active' : '']">이번 달</a></li>
							<li><a href="javascript:void(0)" @click="op('lMonth',10)" v-bind:class="[(this.calListActive === 10) ? 'active' : '']">지난 달</a></li>
							<li><a href="javascript:void(0)" @click="op('set',11)" @click.stop="cls" v-bind:class="[(this.calListActive === 11) ? 'active' : '']">직접 설정</a></li>
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
					<div class="calender-btn-wrap">
						<div class="calender-inner-wrap">
							<p id="date-desc" class="calender-date">{{ this.textDate }}</p>
							<div class="calender-btn">
								<button type="button" class="close_btn" @click.stop="cls">취소</button>
								<button type="button" class="update_btn">업데이트</button>
							</div>
						</div>
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
		  calListActive: null,
		  show: false,
		  dates: this.vi(this.value),
		  textDate:''
		}
	  },
	  computed: {
		range () {
		  return this.dates.length === 2
		},
		text () {
		  const val = this.value
		  const txt = this.dates.map(date => this.tf(date)).join(` ${this.rangeSeparator} `)

		  let startDate = this.dates.map(date => this.tf(date))[0].split('-')
		  let endDate = this.dates.map(date => this.tf(date))[1].split('-')

		  let dateText = startDate[0] + '년' + startDate[1] + '월' + startDate[2] + '일' + ' ~ ' + endDate[0] + '년' + endDate[1] + '월' + endDate[2] + '일'
		  this.textDate = dateText

		  if (Array.isArray(val)) {
			return val.length > 1 ? txt : ''
		  } else {
			return val ? txt : ''
		  }
		},
	  },
	  watch: {
		value (val) {
		  this.dates = this.vi(this.value)
		}
	  },
	  methods: {
	  	op(set,act) {
	  		const today = new Date()


	  		if(set == 'all') {
	  			this.dates[0] = this.syAll().start
	  			this.dates[1] = this.syAll().end
	  		}else if(set == 'today') {
		  		this.dates[0] = today
		  		this.dates[1] = today
	  		}else if(set == '1') {
	  			this.dates[0] = this.wk(1)
	  			this.dates[1] = today
	  		}else if(set == '7') {
	  			this.dates[0] = this.wk(7)
	  			this.dates[1] = today
	  		}else if(set == '14') {
	  			this.dates[0] = this.wk(14)
	  			this.dates[1] = today
	  		}else if(set == '30') {
	  			this.dates[0] = this.wk(30)
	  			this.dates[1] = today
	  		}else if(set == 'tWeek') {
	  			this.dates[0] = this.sw().start
	  			this.dates[1] = this.sw().end
	  		}else if(set == 'lWeek') {
	  			this.dates[0] = this.swP().start
	  			this.dates[1] = this.swP().end
	  		}else if(set == 'tMonth') {
	  			this.dates[0] = this.sm().start
	  			this.dates[1] = this.sm().end
	  		}else if(set == 'lMonth') {
	  			this.dates[0] = this.smP().start
	  			this.dates[1] = this.smP().end
	  		}else{
	  		}
	  		//리스트 액티브
	  		this.calListActive = parseInt(act)
	  		this.ok()
	  	},


	  	//올해 전체
	  	syAll() {
		    let d2
		    let d22
		    d2 = new Date()
		    d22 = new Date(d2.getFullYear() ,"0","1")
		    let d3
		    let d33
		    d3 = new Date()
		    d33 = new Date()
		    return {
		    	'start':d22,
		    	'end':d33
		    }

		},
	  	//~몇일전
	  	wk(time) {
		  const d = new Date()
		  const dayOfMonth = d.getDate()
		  d.setDate(dayOfMonth - time)
		  return d
		},
		//~달전
		mh(time) {
		  const d = new Date()
		  const monthOfYear = d.getMonth()
		  d.setMonth(monthOfYear - time)
		  return d
		},
		//이번주
		sw() {
		    const now = new Date()
		    const nowDayOfWeek = now.getDay()
		    const nowDay = now.getDate()
		    const nowMonth = now.getMonth()
		    let nowYear = now.getFullYear()
		    nowYear += (nowYear < 2000) ? 1900 : 0
		    const weekStartDate = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek)
		    const weekEndDate = new Date(nowYear, nowMonth, nowDay + (6 - nowDayOfWeek))
		    return {
		    	'start':weekStartDate,
		    	'end':weekEndDate
		    }
		},
		//지난주
		swP() {
		    const now = new Date()
		    const nowDayOfWeek = now.getDay() + 6
		    const nowDay = now.getDate()
		    const nowMonth = now.getMonth()
		    let nowYear = now.getFullYear()
		    nowYear += (nowYear < 2000) ? 1900 : 0
		    const weekStartDate = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek - 1)
		    const weekEndDate = new Date(nowYear, nowMonth, nowDay + (5 - nowDayOfWeek))
		    return {
		    	'start':weekStartDate,
		    	'end':weekEndDate
		    }
		},
		//이번달
		sm() {
		    let d2
		    let d22
		    d2 = new Date();
		    d22 = new Date(d2.getFullYear(), d2.getMonth())
		    let d3
		    let d33
		    d3 = new Date();
		    d33 = new Date(d3.getFullYear(), d3.getMonth() + 1, "")
		    return {
		    	'start':d22,
		    	'end':d33
		    }
		},
		//지난달
		smP() {
		    let d2
		    let d22
		    d2 = new Date();
		    d22 = new Date(d2.getFullYear(), d2.getMonth() -1)
		    let d3
		    let d33
		    d3 = new Date();
		    d33 = new Date(d3.getFullYear(), d3.getMonth(), "")
		    return {
		    	'start':d22,
		    	'end':d33
		    }
		},




		//날짜 변환
	    parse (num) {
	      return parseInt(num / 1000)
	    },
	    //서포트 10이하 01식 변환
	    ts(time) {
	    	var supTime = time;
			var returnTime = (supTime < 10) ? '0' + supTime : supTime;
			return returnTime;
	    },


	    cls() {
	    	this.$emit('input', this.range ? [] : '')
	    },
		close () {
		  // this.$emit('input', this.range ? [] : '')
		  this.show = false
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



