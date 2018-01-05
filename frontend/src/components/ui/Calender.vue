<template>
	<div class="vue-calender">

		<vue-datepicker-local v-model="range" rangeSeparator/>

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
		    }
		  }
	}
</script>

<style lang="css" scoped>
</style>