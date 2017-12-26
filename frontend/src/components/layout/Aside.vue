<template>
	<aside>
		<div class="aside_section first_section">
			<div class="user_info_wrap">
				<div class="u_logo"></div>
				<div class="u_info">
					<p id="ad_list_cate" href="javascript:void(0);" onclick="adList(this);">프리메라프리메라</p>
					<p>2138765478123468</p>
				</div>
			</div>
			<div class="user_ad_list">
				<div class="ad_list_category hide">
					<div class="ad_search_wrap">
						<input type="text" placeholder="광고주명을 입력하세요" class="ad_search_box">
						<button class="ad_submit"></button>
					</div>
					<div class="ad_search_list">
						<ul>
							<li>
								<div class="list_image"></div>
								<div class="list_info">
									<strong>프리메라 NEW</strong>
									<div>계정번호 : 1059484622123515</div>
								</div>
							</li>
							<li>
								<div class="list_image"></div>
								<div class="list_info">
									<strong>프리메라 NEW</strong>
									<div>계정번호 : 1059484622123515</div>
								</div>
							</li>
							<li>
								<div class="list_image"></div>
								<div class="list_info">
									<strong>프리메라 NEW</strong>
									<div>계정번호 : 1059484622123515</div>
								</div>
							</li>
							<li>
								<div class="list_image"></div>
								<div class="list_info">
									<strong>프리메라 NEW</strong>
									<div>계정번호 : 1059484622123515</div>
								</div>
							</li>
							<li>
								<div class="list_image"></div>
								<div class="list_info">
									<strong>프리메라 NEW</strong>
									<div>계정번호 : 1059484622123515</div>
								</div>
							</li>
							<li>
								<div class="list_image"></div>
								<div class="list_info">
									<strong>프리메라 NEW</strong>
									<div>계정번호 : 1059484622123515</div>
								</div>
							</li>
						</ul>
					</div>
				</div>
			</div>
		</div>
		<div class="section_tab_widget clearfix">
			<ul>
				<li rel="section_list_1" class="aside_section active"><router-link v-bind:to="{ path: '/TargetPick' }"></router-link></li>
				<li rel="section_list_2" class="aside_section"><router-link v-bind:to="{ path: '/TargetReport' }"></router-link></li>
				<li rel="section_list_3" class="aside_section"><router-link v-bind:to="{ path: '/CreativeLibrary' }"></router-link></li>
			</ul>
		</div>
	</aside>
</template>

<script>
export default {

  name: 'Aside',

  data () {
    return {

    }
  }
}
</script>

<style lang="css" scoped>
</style>