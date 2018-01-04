<template>
	<div class="vue-calender">

		<date-picker :inline="true" name="uniquename" :value="this.date"></date-picker>

	</div>
</template>

<script>
	import Datepicker from 'vuejs-datepicker'
	import DateLanguages from '@/components/utils/DateLanguages'
	const state = {
	  date:new Date(2016, 9,  16)
	}
	export default {
		name: 'Calender',
		components:{'date-picker':Datepicker},
		data () {
			return {
				date:new Date(2016, 9,  16)
			}
		}
	}
</script>

<style lang="css" scoped>
</style>