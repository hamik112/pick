<template>
	<div class="vue-calender">
		<div class="calender-list" v-if="show">
			<ul>
				<li>리스트1</li>
				<li>리스트1</li>
				<li>리스트1</li>
				<li>리스트1</li>
			</ul>
		</div>
		<vue-datepicker-local v-model="range" rangeSeparator></vue-datepicker-local>
		<div class="calender-btn" v-if="show">
			<button type="button">확인</button>
			<button type="button">취소</button>
		</div>
	</div>
</template>

<script>
	import VueDatepickerLocal from 'vue-datepicker-local'
	const state = {
	  date:new Date(2016, 9,  16)
	}
	export default {
		name: 'Calender',
		components: {
		    VueDatepickerLocal
		},
		data () {
			return {
				show: false,
				time: new Date(),
            	range: [new Date(),new Date()],
	            emptyTime: '',
	            emptyRange: [],
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
			}
		},
		methods: {
			disabledDate (time) {
			  return time < this.min || time > this.max
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
.vue-calender { position:relative;
	.calender-list { position:absolute; left:-200px; top:40px; width:200px; height:295px; background-color:#fff; }
	.calender-btn { position:absolute; left:-200px; top:339px; width:100%;}
}





@keyframes datepicker-anim-in {
    0% {
        opacity: 0;
        transform: scaleY(.8)
    }
    to {
        opacity: 1;
        transform: scaleY(1)
    }
}

@keyframes datepicker-anim-out {
    0% {
        opacity: 1;
        transform: scaleY(1)
    }
    to {
        opacity: 0;
        transform: scaleY(.8)
    }
}
</style>