<template>
	<div class="modal-mask">
		<div class="modal-wrapper">
			<div class="modal-container">
				<div class="layer-pop-widget">
					<div class="popup-widget" id="target_pop_01">
						<div class="popup-contents clearfix">
							<div class="pop_title_wrap">
								<div class="pop_title">타겟 만들기 (<span id="page-number">1</span>/2)</div>
								<p class="popup-btn"><button type="button" id="close-btn" class="close_pop close-btn" @click="$emit('close')"><img src="../../assets/images/target/white_close_i.png" alt=""></button></p>
							</div>
							<div class="pop_tab_wrap clearfix" v-if="tabActive1">
								<div class="cate_contents_widget">
									<ul class="target_pick_01">
										<li @click="tabMove(1)">
											<span>사이트방문</span>
										</li>
										<li @click="tabMove(1)">
											<span>특정페이지 방문</span>
										</li>
										<li @click="tabMove(1)">
											<span>NEO 타겟</span>
										</li>
										<li @click="tabMove(1)">
											<span>구글애널리틱스</span>
										</li>
									</ul>
									<ul class="target_pick_02">
										<li @click="tabMove(1)">
											<span>구매</span>
										</li>
										<li @click="tabMove(1)">
											<span>장바구니</span>
										</li>
										<li @click="tabMove(1)">
											<span>회원가입</span>
										</li>
										<li @click="tabMove(1)">
											<span>단계별 전환</span>
										</li>
									</ul>
								</div>
								<div class="btn_wrap">
									<button type="button" class="close_pop" @click="$emit('close')">취소</button>
								</div>
							</div>

							<div class="target_contents_wrap pop-scroll clearfix" v-if="tabActive2">
								<div class="target_contents_inner">
									<div class="target_thead">
										<div class="main_title">
											<div><img src="../../assets/images/target/neo_logo.png" alt="neo"></div>
											<div class="title_info">
												<p>NEO타겟</p>
												<p>타겟의 속성을 정의하세요</p>
											</div>
										</div>
										<div class="use_wrap">
											<div class="use_select">
												<div class="contents_title">사용픽셀</div>
												<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
											</div>
											<div class="use_date">
												<div>수집기간 : 최근</div>
												<div><input type="text"><span>일</span></div>
											</div>
										</div>
										<div class="target_name">
											<div class="contents_title">타겟이름</div>
											<div><input type="text"></div>
										</div>
										<div class="target_data">
											<div class="contents_title">타겟 모수</div>
											<div>
												<span>12,000</span>명
											</div>
										</div>
										<div class="target_type">
											<div class="contents_title">Neo 유형</div>
											<ul>
												<li>
													<div class="result_check"><input type="checkbox" id="target_type01"><label for="target_type01">매체</label></div>
												</li>
												<li>
													<div class="result_check"><input type="checkbox" id="target_type02"><label for="target_type02">그룹</label></div>
												</li>
												<li>
													<div class="result_check"><input type="checkbox" id="target_type03"><label for="target_type03">키워드</label></div>
												</li>
												<li>
													<div class="result_check"><input type="checkbox" id="target_type04"><label for="target_type04">엑셀업로드</label></div>
												</li>
											</ul>
										</div>
									</div>
									<div class="target_tbody">
										<div class="target_inner_tbody clearfix">
											<div class="cate_contents">
												<div class="account_info">
													<div class="account_title">"아래 그룹로 유입된 사람"중</div>
													<div>
														<ui-select :selectData="this.selectData2" :onClick="selectTarget"></ui-select>
													</div>
													<div class="account_date">
														<input type="text"><span>일</span>
													</div>
												</div>
												<div class="account_wrap">
													<div class="account_inner_wrap clearfix">
														<div class="account_left">
															<div class="advertiser_search_result pop-scroll">
																<div class="result_list_inner">
																	<div class="result_thead">
																		<ul>
																			<li>
																				<div class="result_check"><input type="checkbox" id="all_check" v-model="selectAll"><label for="all_check"></label></div>
																				<div class="result_account">계정명</div>
																				<div class="result_group">그룹명</div>
																				<div class="result_switch">전환 수</div>
																			</li>
																		</ul>
																	</div>
																	<div class="result_tbody">
																		<ul id="adv-list-1">
																			<li v-for="adv in advs">
																				<div class="result_check"><input type="checkbox" v-model="selected" :value="adv.id" class="result-checkbox" :data-type="'advs'" :data-id="adv.type_id" :id="'adv-check-' + adv.id"><label :for="'adv-check-' + adv.id"></label></div>
																				<div class="result_account">LF몰</div>
																				<div class="result_group">LF_M_구글</div>
																				<div class="result_switch">LF_M_구글</div>
																			</li>
																		</ul>
																	</div>
																</div>
															</div>
															<div class="account_add_wrap">
																<div>*최근 한달 기준</div>
																<button type="button" v-on:click="checkList('advs','addAdvs')">선택한 매체 추가</button>
															</div>
														</div>
														<div class="account_right clearfix">
															<button><img src="../../assets/images/target/target_close_btn.png" alt=""></button>
															<ul>
																<li v-for="addAdv in addAdvs" class="sticker_btn">
																	<span>모바일 DA_페이스북 (질바이질슈즈)</span> <span><img src="images/target/target_list_close.png" alt=""></span>
																</li>
															</ul>
														</div>
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>
								<div class="btn_wrap">
									<button class="before_btn close_pop" @click="tabMove(0)">취소</button>
									<button class="next_btn">타겟 만들기</button>
								</div>
								<div class="btn_wrap">
									<button class="before_btn close_pop" @click="$emit('close')">취소</button>
									<button class="delete_btn">타겟 삭제</button>
									<button class="adjust_btn">타겟 수정</button>
								</div>
							</div>

						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

</template>

<script>

// UI
import Select from '@/components/ui/Select'

export default {

  name: 'TargetMake01',
  components:{
  	'ui-select': Select
  },
  data () {
    return {
    	tabActive1:true,
    	tabActive2:false,
    	categoryName:'',

    	selectData: {
          emptyText: '전체보기',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },
        selectData2: {
          emptyText: '특정일 동안 미방문 고객',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },
        advs:[
        	{ "id": "1", "name": "LF몰", "advid": "LF_M_구글1", "type_id":"13" },
		    { "id": "2", "name": "LF몰2", "advid": "LF_M_구글2", "type_id":"11" },
		    { "id": "3", "name": "LF몰3", "advid": "LF_M_구글3", "type_id":"15" },
		    { "id": "4", "name": "LF몰4", "advid": "LF_M_구글4", "type_id":"17" }
        ],
        addAdvs:[],
        checkData:[],
        selected:[]
    }
  },
  methods: {
	tabMove(activeNumber, beforeNumber) {
		let tabArray = ['tabActive1','tabActive2']
		let pageNum = (activeNumber == 0) ? '1':'2'

		document.getElementById('page-number').innerText = pageNum

		for(let i = 0; i < tabArray.length; i++) {
			if(i == activeNumber) {
				this[tabArray[i]] = true
			}else{
				this[tabArray[i]] = false
			}
		}
	},
	selectTarget: function (item) {
		this.selectData.emptyText = item
	},
	allCheck(value,key1,key2,before,after) {
		const me = this
		var selected = []
        if (value) {
            this.checkFilter(key1, 'type2')
            me[key1].forEach(function (item) {
                selected.push(item.id)
            });
        }
        me[key2] = selected;
	},
	checkList (before,after) {
		const me = this

		this.checkFilter(before, 'type1')

		me[after] = me[after].concat(me.checkData)
		me.checkData.forEach(function(value, index) {
			me[before] = me[before].filter(function(item) {
				return item !== value
			})
		})

		this.selected = []
		me.checkData = []
	},
	checkFilter(type, type2) {
		let elId = "adv-list-1"
		let ul = document.getElementById(elId)
		let items = ul.getElementsByTagName("li")
		let itemsData = this[type]

		for (let i = 0; i < items.length; i++) {
			let checkBox = items[i].getElementsByTagName('input')[0].checked
			if(checkBox == true) {
				let checkItemsId = items[i].getElementsByTagName('input')[0].getAttribute('data-id')
				for(let idx = 0; idx < itemsData.length; idx++) {
					if(checkItemsId == itemsData[idx]['type_id']) {
						this.checkData.push(itemsData[idx])
					}
				}
			}
		}
	}
  },
  computed:{
  	selectAll: {
        get: function () {
            let advKeys = Object.keys(this.advs)
        	if(advKeys.length != 0) {
            	return this.advs ? this.selected.length == advKeys.length : false;
            }
        },
        set: function (value) {
            this.allCheck(value,'advs','selected','advs','addAdvs')
        }
    }
  }

}
</script>

<style lang="css" scoped>
</style>
