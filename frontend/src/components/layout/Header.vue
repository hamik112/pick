<template>
	<header>


		<transition name='modal'>
			<SetupPop v-if="setupOn" @close="setupOn = false"></SetupPop>
		</transition>


		<div class="left_area"><a href="#/"><img src="../../assets/images/common/main_logo.jpg" alt="pickdata" /></a></div>
		<div class="right_area">
			<div class="user">
				<p class="user_mask"></p>
				<p class="user_image"><img src="../../assets/images/common/test_img.jpg" alt=""></p>
				<p>임준수</p>
			</div>
			<div class="user_setup" tabindex="-1" @blur="allCategory('blur')">
				<p id="set_up" v-on:click="allCategory()"><img src="../../assets/images/icon/set_up_btn.png" alt="톱니바퀴" /></p>
				<div class="setup_list" v-if="settingDes">
					<p @click="setupOn = true">설정</p>
					<p>로그아웃</p>
				</div>
			</div>
		</div>
	</header>
</template>

<script>


import SetupPop from '@/components/popup/Advertising_setup'


export default {
  name: 'Header',
  components:{
  	'SetupPop':SetupPop
  },
  methods:{
  	allCategory:function(type) {
  		if(type != 'blur') {
  			this.settingDes = !this.settingDes
  		}else{
  			this.settingDes = false
  		}
  	}
  },
  data () {
    return {
    	setupOn:false,
    	settingDes:false
    }
  }
}
</script>

<style lang="css" scoped>
	.user_setup { margin-left:44px; padding-left:0px !important; }
	#set_up { cursor:pointer; }
</style>
