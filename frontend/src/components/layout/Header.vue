<template>
	<header>
		<div class="left_area"><a href="#/"><img src="../../assets/images/common/main_logo.jpg" alt="pickdata" /></a></div>
		<div class="right_area">
			<div class="user">
				<p><img src="../../assets/images/icon/user_logo.png" alt=""></p>
				<p>임준수</p>
			</div>
			<div class="user_setup">
				<a id="set_up" href="javascript:void(0);" v-on:click="allCategory()"><img src="../../assets/images/icon/set_up_btn.png" alt="톱니바퀴" /></a>
				<div class="setup_list" v-if="settingDes">
					<p>설정</p>
					<p>로그아웃</p>
				</div>
			</div>
		</div>
	</header>
</template>

<script>
export default {
  name: 'header',
  methods:{
  	allCategory:function() {
  		this.settingDes = !this.settingDes;
  	}
  },
  data () {
    return {
    	settingDes:false
    }
  }
}
</script>

<style lang="css" scoped>
</style>