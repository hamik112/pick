<template>
	<header>




		<div class="left_area"><a href="#/"><img src="../../assets/images/common/main_logo.jpg" alt="pickdata" /></a></div>
		<div class="right_area">
			<div class="user">
				<p class="user_mask"></p>
				<p class="user_image"><img v-bind:src="userImage" alt=""></p>
				<p>{{ userName }}</p>
			</div>
			<div class="user_setup">
				<p id="set_up"><router-link v-bind:to="{ path: '/setting' }"><img src="../../assets/images/icon/set_up_btn.png" alt="톱니바퀴" /></router-link></p>
				<div class="setup_list">
					<p><router-link v-bind:to="{ path: '/setting' }">설정</router-link></p>
					<p><a href="javascript:void(0)" @click="logout">로그아웃</a></p>
				</div>
			</div>
		</div>
	</header>
</template>

<script>

import { getUserName, getUserImage } from '../../utils/auth'
import SetupPop from '@/components/popup/Advertising_setup'


export default {
	name: 'Header',

	components:{
		'SetupPop': SetupPop
	},

	mounted () {
		this.userName = getUserName()
		this.userImage = getUserImage()
	},

	methods:{
		logout(){
	  		if(confirm('픽데이터에서 로그아웃 하시겠습니까?') == true) {

	  		}else{
	  			return
	  		}
	  	}
	},

	data () {
		return {
			setupOn: false,
			userName: '',
			userImage: ''
		}
	}
}
</script>

<style lang="css" scoped>
.user_setup { margin-left:44px; padding-left:0px !important; }
#set_up { cursor:pointer; }
</style>
