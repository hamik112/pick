<template>
	<div class="modal-mask">
		<div class="modal-wrapper">
			<div class="modal-container">
				<div class="layer-pop-widget">
					<div class="popup-widget" id="ad_set_pop_1">
						<div class="popup-contents">
							<div class="pop_title_wrap">
								<div class="pop_title">광고계정 설정하기</div>
								<p class="popup-btn"><button type="button" id="close-btn" class="close_pop close-btn" @click="$emit('close')"><img src="../../assets/images/target/white_close_i.png" alt=""></button></p>
							</div>
							<div class="ad_info_wrap">
								<div class="ad_mask"></div>
								<div class="ad_image"><img src="../../assets/images/common/test_img.jpg" alt=""></div>
								<div class="ad_info">
									<strong>프리메라 NEW</strong>
									<div>계정번호:1059484622123515</div>
								</div>
							</div>
							<div class="list-tab-widget">
								<div class="tab-nav-widget">
									<ul>
										<li rel="tab-list-1" v-bind:class="[(this.tabListStep === 0) ? 'active' : '']">
											<p></p>
											<a href="javascript:void(0);"><span>1</span>카테고리 설정</a>
										</li>
										<li rel="tab-list-2" v-bind:class="[(this.tabListStep === 1) ? 'active' : '']">
											<p></p>
											<a href="javascript:void(0);"><span>2</span>네오 계정 연동</a>
										</li>
										<li rel="tab-list-3" v-bind:class="[(this.tabListStep === 2) ? 'active' : '']">
											<p></p>
											<a href="javascript:void(0);"><span>3</span>픽셀 이벤트 매핑</a>
										</li>
									</ul>
								</div>
								<div class="pop_tab_wrap">
									<div class="tab-contents-widget">

										<!-- 카테고리 설정 -->
										<div id="tab-list-1" class="basic-tab-contents category_setup clearfix" v-if='tabActive1'>
											<div class="cate_prologue">
												<strong>현재 선택된 광고 계정의 카테고리를 지정해주세요</strong>
												<p>통계 및 계정 유형 분석을 위해 반드시 선택하셔야 합니다.</p>
											</div>
											<div class="cate_contents_widget">
												<ul class="target_pick_01">
													<li @click="clickSteop1Category('보험')" v-bind:class="[(this.categoryName === '보험') ? 'Click_on' : '']">
														<span>보험</span>
													</li>
													<li @click="clickSteop1Category('대출')" v-bind:class="[(this.categoryName === '대출') ? 'Click_on' : '']">
														<span>대출</span>
													</li>
													<li @click="clickSteop1Category('카드')" v-bind:class="[(this.categoryName === '카드') ? 'Click_on' : '']">
														<span>카드</span>
													</li>
													<li @click="clickSteop1Category('NGO')" v-bind:class="[(this.categoryName === 'NGO') ? 'Click_on' : '']">
														<span>NGO</span>
													</li>
												</ul>
												<ul class="target_pick_02">
													<li @click="clickSteop1Category('쇼핑몰')" v-bind:class="[(this.categoryName === '쇼핑몰') ? 'Click_on' : '']">
														<span>쇼핑몰</span>
													</li>
													<li @click="clickSteop1Category('여행')" v-bind:class="[(this.categoryName === '여행') ? 'Click_on' : '']">
														<span>여행</span>
													</li>
													<li @click="clickSteop1Category('뷰티')" v-bind:class="[(this.categoryName === '뷰티') ? 'Click_on' : '']">
														<span>뷰티</span>
													</li>
													<li @click="clickSteop1Category('기타')" v-bind:class="[(this.categoryName === '기타') ? 'Click_on' : '']">
														<span>기타</span>
													</li>
												</ul>
											</div>
											<div class="btn_wrap">
												<button type="button" class="next_btn" @click="tabMove('1', '0')">다음</button>
											</div>
										</div>
										<!-- /.카테고리 설정 -->


										<!-- 네오 계정 연동 -->
										<div id="tab-list-2" class="basic-tab-contents clearfix" v-if='tabActive2'>
											<div class="cate_prologue">
												<strong>연결될 네오 계정을 선택해 주세요.</strong>
												<p>연결 가능한 네오 계정이 없다면 다음을 클릭해 주세요.</p>
											</div>

											<div class="cate_contents">
												<div class="account_wrap">
													<div class="advertiser_search">
														<div class="search_title">광고주검색</div>
														<div><input type="text"></div>
														<div><button>조회</button></div>
													</div>
													<div class="advertiser_search_result pop-scroll">
														<div>
															<div class="result_thead">
																<ul>
																	<li>
																		<div class="result_check"><input type="checkbox" id="all_check" v-model="selectAll"><label for="all_check"></label></div>
																		<div class="result_advertiser">광고주</div>
																		<div class="result_account">계정명</div>
																	</li>
																</ul>
															</div>
															<div class="result_tbody">
																<ul>
																	<li v-for="adv in advs">
																		<div class="result_check"><input type="checkbox" v-model="selected" :value="adv.id" class="result-checkbox" :data-key="'list' + adv.id" :id="'adv-check-' + adv.id" @change="handleChange(adv)"><label :for="'adv-check-' + adv.id"></label></div>
																		<div class="result_advertiser">{{ adv.name }}</div>
																		<div class="result_account">{{ adv.advid }}</div>
																	</li>
																</ul>
															</div>
														</div>
													</div>
												</div>
												<div class="interlock_btn">
													<button type="button" v-on:click="checkList('addAdvs','advs')"><img src="../../assets/images/icon/account_left.jpg" alt=""></button>
													<button type="button" v-on:click="checkList('advs','addAdvs')"><img src="../../assets/images/icon/account_right.jpg" alt=""></button>
												</div>
												<div class="account_wrap">
													<div class="advertiser_search">
														<div class="search_title">연결계정 <span>2</span></div>
													</div>
													<div class="advertiser_search_result pop-scroll">
														<div>
															<div class="result_thead">
																<ul>
																	<li>
																		<div class="result_check"><input type="checkbox" id="right_all_check" v-model="addSelectAll"><label for="right_all_check"></label></div>
																		<div class="result_advertiser">광고주</div>
																		<div class="result_account">계정명</div>
																	</li>
																</ul>
															</div>
															<div class="result_tbody">
																<ul>
																	<li v-for="addAdv in addAdvs">
																		<div class="result_check"><input type="checkbox" v-model="addSelected" :value="addAdv.id" class="result-checkbox" :id="'addAdv-check-' + addAdv.id" @change="handleChange(addAdv)"><label :for="'addAdv-check-' + addAdv.id"></label></div>
																		<div class="result_advertiser">{{ addAdv.name }}</div>
																		<div class="result_account">{{ addAdv.advid }}</div>
																	</li>
																</ul>
															</div>
														</div>
													</div>
												</div>
											</div>


											<div class="btn_wrap">
												<button class="before_btn" @click="tabMove('0', '1')">이전</button>
												<button type="button" class="next_btn" @click="tabMove('2', '1')">다음</button>
											</div>
										</div>
										<!-- /.네오 계정 연동 -->



										<!-- 픽셀 이벤트 매핑 -->
										<div id="tab-list-3" class="basic-tab-contents clearfix" v-if='tabActive3'>
											<div class="cate_prologue">
												<strong>광고 계정에 사용된 픽셀 이벤트를 매핑해 주세요.</strong>
												<p>픽셀 이벤트를 매핑해 주시면, 좀 더 편리한 맞춤 타겟팅을 사용할 수 있습니다.</p>
											</div>
											<div class="event_mapping_wrap">
												<ul>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
												</ul>
												<div class="btn_wrap">
													<button type="button" class="before_btn" @click="tabMove('1', '2')">이전</button>
													<button class="next_btn" @click="success">완료</button>
												</div>
											</div>
										</div>
										<!-- /.픽셀 이벤트 매핑 -->


									</div>
								</div>
							</div>
							<p class="popup-btn"><button type="button" id="close-btn" class="close-btn close_pop"><img src="../../assets/images/target/white_close_i.png" alt=""></button></p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

</template>

<script>
//UI
import Select from '@/components/ui/Select'

export default {
	name:'SetupPop',

	components:{
		'ui-select':Select
	},

	data () {
		return {
			tabActive1: true,
			tabActive2: false,
			tabActive3: false,

			categorySelectData: {
				emptyText: '픽셀 이벤트를 선택해주세요',
				textList: [
					'픽셀1',
					'픽셀2',
					'픽셀3'
				]
			},
			advs: [
			    { "id": "1", "name": "LF몰", "advid": "LF_M_구글1" },
			    { "id": "2", "name": "LF몰2", "advid": "LF_M_구글2" },
			    { "id": "3", "name": "LF몰3", "advid": "LF_M_구글3" },
			    { "id": "4", "name": "LF몰4", "advid": "LF_M_구글4" }
			],
			addAdvs:[],
			checkData:[],
			addKey:[],
			selected: [],
			addSelected:[],

			tabListStep: 0,
			categoryName: ''
		}
	},

	methods:{
		clickSteop1Category (name) {
			this.categoryName = name
		},
		selectCategory (item) {
			this.categorySelectData.emptyText = item
		},
		handleChange (item) {
			let checked = event.target.checked
			if(checked == true) {
				this.checkData.push(item)
			}
		},
		checkList (before,after) {
			const me = this
			me[after] = me[after].concat(me.checkData)

			me.checkData.forEach(function(value, index) {
				me[before] = me[before].filter(function(item) {
					return item !== value
				})
			})
			this.addSelected = []
			this.selected = []
			me.checkData = []
		},
		allCheck(value,key1,key2,before,after) {
			const me = this
			var selected = []

            if (value) {
                me[key1].forEach(function (item) {
                    selected.push(item.id)
                    me.checkData.push(item)
                });
            }
            me[key2] = selected;
		},
		tabMove (activeNumber, beforeNumber) {
			if (beforeNumber === '0') {
				if (this.categoryName === '') {
					alert('추후 카테고리 선택을 해야만 하게 수정필요.')
					// return
				}
			}
			this.tabListStep = parseInt(activeNumber)
			let tabArray = ['tabActive1','tabActive2','tabActive3']
			for(let i = 0; i < tabArray.length; i++) {
				if(i == activeNumber) {
					this[tabArray[i]] = true
				}else{
					this[tabArray[i]] = false
				}
			}
		},
		success () {
			alert('설정이 완료되었습니다.');
			this.$emit('close')
		}
	},

	computed: {
		selectAll: {
	        get: function () {
                return this.advs ? this.selected.length == this.advs.length : false;
            },
            set: function (value) {
                this.allCheck(value,'advs','selected','advs','addAdvs')
            }
	    },
	    addSelectAll:{
	        get: function () {
	        	let advKeys = Object.keys(this.addAdvs)
	        	if(advKeys.length != 0) {
	            	return this.addAdvs ? this.addSelected.length == advKeys.length : false;
	            }
	        },
	        set: function (value) {
	            this.allCheck(value,'addAdvs','addSelected','addAdvs','advs')
	        }
	    }
	}
}
</script>

<style lang="css" scoped>
</style>
