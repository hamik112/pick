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

              <!-- 카테고리 선택 탭 -->
              <div class="pop_tab_wrap clearfix" v-if="tabAction.tabActive1.show">
                <div class="cate_contents_widget">
                  <ul class="target_pick_01">
                    <li @click="tabMove(1)">
                      <span>사이트방문</span>
                    </li>
                    <li @click="tabMove(2)">
                      <span>특정페이지 방문</span>
                    </li>
                    <li @click="tabMove(3)">
                      <span>NEO 타겟</span>
                    </li>
                    <li @click="tabMove(4)">
                      <span>구글애널리틱스</span>
                    </li>
                  </ul>
                  <ul class="target_pick_02">
                    <li @click="tabMove(5)">
                      <span>구매</span>
                    </li>
                    <li @click="tabMove(6)">
                      <span>장바구니</span>
                    </li>
                    <li @click="tabMove(7)">
                      <span>회원가입</span>
                    </li>
                    <li @click="tabMove(8)">
                      <span>단계별 전환</span>
                    </li>
                  </ul>
                </div>
                <div class="btn_wrap">
                  <button type="button" class="close_pop" @click="$emit('close')">취소</button>
                </div>
              </div>


              <!-- 사이트 방문 탭 -->
              <div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive2.show">
                <div class="target_contents_inner">
                  <div class="target_thead">
                    <div class="main_title">
                      <div><img src="../../assets/images/target/target_logo_01.png" alt="neo"></div>
                      <div class="title_info">
                        <p>사이트방문</p>
                        <p>타겟의 속성을 정의하세요</p>
                      </div>
                    </div>
                    <div class="use_wrap">
                      <div class="use_select">
                        <div class="contents_title">사용픽셀</div>
                        <ui-select :selectData="this.select1" data-key="select1" :onClick="selectTarget"></ui-select>
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
                  </div>
                  <div class="target_tbody">
                    <div class="target_inner_tbody clearfix">
                      <div class="target_generate">
                        <div class="account_info">
                          <div class="account_title">"사이트 방문자"중</div>
                          <div>
                            <ui-select :selectData="this.selectUser" data-key="selectUser" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subSelect">
                          <ui-select :selectData="this.selectSub" data-key="selectSub" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subInput">
                            <input type="text" v-if="subInput"><span>일</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="btn_wrap">
                  <button class="before_btn close_pop" @click="tabMove(0)">취소</button>
                  <button class="next_btn" @click="createVisitSite()">타겟 만들기</button>
                </div>
              </div>

              <!-- 특정 페이지 방문 탭 -->
              <div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive3.show">
                <div class="target_contents_inner">
                  <div class="target_thead">
                    <div class="main_title">
                      <div><img src="../../assets/images/target/target_logo_02.png" alt="neo"></div>
                      <div class="title_info">
                        <p>특정페이지 방문</p>
                        <p>타겟의 속성을 정의하세요</p>
                      </div>
                    </div>
                    <div class="use_wrap">
                      <div class="use_select">
                        <div class="contents_title">사용픽셀</div>
                        <ui-select :selectData="this.select3" data-key="select3" :onClick="selectTarget"></ui-select>
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
                  </div>
                  <div class="target_tbody">
                    <div class="target_inner_tbody clearfix">
                      <div class="target_generate">
                        <div class="account_info">
                          <div class="account_title">"아래 그룹로 유입된 사람"중</div>
                          <div>
                            <ui-select :selectData="this.selectUser" data-key="selectUser" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subSelect">
                          <ui-select :selectData="this.selectSub" data-key="selectSub" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subInput">
                            <input type="text" v-if="subInput"><span>일</span>
                          </div>
                        </div>
                        <div class="generate_url_list">

                          <div v-for="(item, index) in fields" class="url_list clearfix">
                            <div class="url_select clearfix">
                              <ui-select :selectData="item.select" :data-key="index" :onClick="multiSelect"></ui-select>
                            </div>
                            <div class="url_input">
                              <input type="text">
                            </div>
                            <div class="url_btn clearfix">
                              <div class="add"><button type="button" @click="fieldBtn(item,'add')">+</button></div>
                              <div class="del" v-if="index > 0"><button type="button" @click="fieldBtn(item,'del')">-</button></div>
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
              </div>

              <!-- 네오 탭 -->
              <div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive4.show">
                <div class="target_contents_inner">
                  <div class="target_thead">
                    <div class="main_title">
                      <div><img src="../../assets/images/target/target_logo_03.png" alt="neo"></div>
                      <div class="title_info">
                        <p>NEO타겟</p>
                        <p>타겟의 속성을 정의하세요</p>
                      </div>
                    </div>
                    <div class="use_wrap">
                      <div class="use_select">
                        <div class="contents_title">사용픽셀</div>
                        <ui-select :selectData="this.select6" data-key="select6" :onClick="selectTarget"></ui-select>
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
                          <div class="result_check"><input type="radio" id="target_type01" @change="wTabs(0,'wTab')" name="neo_type" value="media" checked><label for="target_type01">매체</label></div>
                        </li>
                        <li>
                          <div class="result_check"><input type="radio" id="target_type02" name="neo_type" @change="wTabs(1,'wTab')" value="group"><label for="target_type02">그룹</label></div>
                        </li>
                        <li>
                          <div class="result_check"><input type="radio" id="target_type03" name="neo_type"  @change="wTabs(2,'wTab')" value="keyword"><label for="target_type03">키워드</label></div>
                        </li>
                        <li>
                          <div class="result_check"><input type="radio" id="target_type04" name="neo_type" @change="wTabs(3,'wTab')" value="excel"><label for="target_type04">엑셀업로드</label></div>
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div class="target_tbody">
                    <div class="target_inner_tbody clearfix">
                      <!-- 매체 -->
                      <div class="cate_contents" v-if="wTab.tab1">
                        <div class="account_info target_generate">
                          <div class="account_title">"아래 매체로 유입된 사람"중</div>
                          <div>
                            <ui-select :selectData="this.selectUser" data-key="selectUser" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subSelect">
                          <ui-select :selectData="this.selectSub" data-key="selectSub" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subInput">
                            <input type="text" v-if="subInput"><span>일</span>
                          </div>
                        </div>
                        <div class="account_wrap account_wrapper">
                          <div class="account_inner_wrap clearfix">
                            <div class="account_left">
                              <div class="advertiser_search_result pop-scroll">
                                <div class="result_list_inner">
                                  <div class="result_thead">
                                    <ul>
                                      <li>
                                        <div class="result_check"><input type="checkbox" id="all_check" v-model="selectAll"><label for="all_check"></label></div>
                                        <div class="result_account">계정명</div>
                                        <div class="result_group">캠페인명</div>
                                        <div class="result_switch">전환 수</div>
                                      </li>
                                    </ul>
                                  </div>
                                  <div class="result_tbody">
                                    <ul id="adv-list-1">
                                      <li v-for="adv in advs">
                                        <div class="result_check"><input type="checkbox" v-model="selected" :value="adv.number" class="result-checkbox" :data-type="'advs'" :data-id="adv.type_id" :id="'adv-check-' + adv.number"><label :for="'adv-check-' + adv.number"></label></div>
                                        <div class="result_account">{{ adv.name }}</div>
                                        <div class="result_group">{{ adv.campaign }}</div>
                                        <div class="result_switch">{{ adv.count }}</div>
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
                              <button type="button" v-on:click="deleteAddAdvs('all')" title="전체삭제"><img src="../../assets/images/target/target_close_btn.png" alt=""></button>
                              <ul id="adv-list-2">
                                <li v-for="addAdv in addAdvs" class="sticker_btn">
                                  <span>{{ addAdv.name }}</span> <span @click="deleteAddAdvs(addAdv)" :data-number="addAdv.number" title="삭제하기"><img src="../../assets/images/target/target_list_close.png" alt=""></span>
                                </li>
                              </ul>
                            </div>
                          </div>
                        </div>
                      </div>
                      <!-- 그룹 -->
                      <div class="cate_contents" v-if="wTab.tab2">
                        <div class="account_info target_generate">
                          <div class="account_title">"아래 그룹로 유입된 사람"중</div>
                          <div>
                            <ui-select :selectData="this.selectUser" data-key="selectUser" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subSelect">
                          <ui-select :selectData="this.selectSub" data-key="selectSub" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subInput">
                            <input type="text" v-if="subInput"><span>일</span>
                          </div>
                        </div>
                        <div class="account_wrap account_wrapper">
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
                                        <div class="result_check"><input type="checkbox" v-model="selected" :value="adv.number" class="result-checkbox" :data-type="'advs'" :data-id="adv.type_id" :id="'adv-check-' + adv.number"><label :for="'adv-check-' + adv.number"></label></div>
                                        <div class="result_account">{{ adv.name }}</div>
                                        <div class="result_group">{{ adv.campaign }}</div>
                                        <div class="result_switch">{{ adv.count }}</div>
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
                              <button type="button" v-on:click="deleteAddAdvs('all')" title="전체삭제"><img src="../../assets/images/target/target_close_btn.png" alt=""></button>
                              <ul id="adv-list-2">
                                <li v-for="addAdv in addAdvs" class="sticker_btn">
                                  <span>{{ addAdv.name }}</span> <span @click="deleteAddAdvs(addAdv)" :data-number="addAdv.number" title="삭제하기"><img src="../../assets/images/target/target_list_close.png" alt=""></span>
                                </li>
                              </ul>
                            </div>
                          </div>
                        </div>
                      </div>
                      <!-- 키워드 -->
                      <div class="cate_contents" v-if="wTab.tab3">
                        <div class="account_info target_generate">
                          <div class="account_title">"아래 키워드로 유입된 사람"중</div>
                          <div>
                            <ui-select :selectData="this.select9" data-key="select9" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subSelect">
                          <ui-select :selectData="this.selectSub" data-key="selectSub" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subInput">
                            <input type="text" v-if="subInput"><span>일</span>
                          </div>
                        </div>
                        <div class="account_wrap account_wrapper">
                          <div class="account_inner_wrap clearfix">
                            <div class="account_left">
                              <div class="advertiser_search_result pop-scroll">
                                <div class="result_list_inner">
                                  <div class="result_thead">
                                    <ul>
                                      <li>
                                        <div class="result_check"><input type="checkbox" id="all_check" v-model="selectAll"><label for="all_check"></label></div>
                                        <div class="result_account">그룹명</div>
                                        <div class="result_group">키워드</div>
                                        <div class="result_switch">전환 수</div>
                                      </li>
                                    </ul>
                                  </div>
                                  <div class="result_tbody">
                                    <ul id="adv-list-1">
                                      <li v-for="adv in advs">
                                        <div class="result_check"><input type="checkbox" v-model="selected" :value="adv.number" class="result-checkbox" :data-type="'advs'" :data-id="adv.type_id" :id="'adv-check-' + adv.number"><label :for="'adv-check-' + adv.number"></label></div>
                                        <div class="result_account">{{ adv.name }}</div>
                                        <div class="result_group">{{ adv.campaign }}</div>
                                        <div class="result_switch">{{ adv.count }}</div>
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
                              <button type="button" v-on:click="deleteAddAdvs('all')" title="전체삭제"><img src="../../assets/images/target/target_close_btn.png" alt=""></button>
                              <ul id="adv-list-2">
                                <li v-for="addAdv in addAdvs" class="sticker_btn">
                                  <span>{{ addAdv.name }}</span> <span @click="deleteAddAdvs(addAdv)" :data-number="addAdv.number" title="삭제하기"><img src="../../assets/images/target/target_list_close.png" alt=""></span>
                                </li>
                              </ul>
                            </div>
                          </div>
                        </div>
                      </div>
                      <!-- 엑셀 -->
                      <div class="cate_contents target_excel" v-if="wTab.tab4">
                        <div class="account_info target_generate">
                          <div class="account_title">"아래 등록 양식으로 유입된 사람"중</div>
                          <div>
                            <ui-select :selectData="this.selectUser" data-key="selectUser" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subSelect">
                          <ui-select :selectData="this.selectSub" data-key="selectSub" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subInput">
                            <input type="text" v-if="subInput"><span>일</span>
                          </div>
                        </div>
                        <div class="account_wrap account_wrapper">
                          <div class="account_inner_wrap clearfix">
                            <div class="account_left">
                              <strong>양식에 맞추어 엑셀을 입력해 주세요.</strong>
                              <p>양식에 맞추어 엑셀을 업로드 해주시면,</p>
                              <p>해당 파라미터를 타겟으로 만들 수 있습니다.</p>
                              <div class="excel_wrap">
                                <div class="download_wrap clearfix">
                                  <button><strong>엑셀업로드</strong></button>
                                  <button>양식 다운로드</button>
                                </div>
                                <div class="input_wrap clearfix">
                                  <div>
                                    <input type="text">
                                  </div>
                                  <button></button>
                                </div>
                                <button class="upload_btn view_alert"><strong>업로드</strong></button>
                              </div>
                            </div>
                            <div class="account_right clearfix">
                              <button type="button" v-on:click="deleteAddAdvs('all')" title="전체삭제"><img src="../../assets/images/target/target_close_btn.png" alt=""></button>
                              <ul id="adv-list-2">
                                <li v-for="addAdv in addAdvs" class="sticker_btn">
                                  <span>{{ addAdv.name }}</span> <span @click="deleteAddAdvs(addAdv)" :data-number="addAdv.number" title="삭제하기"><img src="../../assets/images/target/target_list_close.png" alt=""></span>
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
                <!-- <div class="btn_wrap">
                  <button class="before_btn close_pop" @click="$emit('close')">취소</button>
                  <button class="delete_btn">타겟 삭제</button>
                  <button class="adjust_btn">타겟 수정</button>
                </div> -->
              </div>

              <!-- 구글애널리틱스 탭 -->
              <div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive5.show">
                <div class="target_contents_inner">
                  <div class="target_thead">
                    <div class="main_title">
                      <div><img src="../../assets/images/target/target_logo_04.png" alt="neo"></div>
                      <div class="title_info">
                        <p>구글애널리틱스</p>
                        <p>타겟의 속성을 정의하세요</p>
                      </div>
                    </div>
                    <div class="use_wrap">
                      <div class="use_select">
                        <div class="contents_title">사용픽셀</div>
                        <ui-select :selectData="this.select21" data-key="select21" :onClick="selectTarget"></ui-select>
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
                  </div>
                  <div class="target_tbody">
                    <div class="target_inner_tbody google_body clearfix">
                      <div class="target_generate google_analytics">
                        <div class="account_info">
                          <div class="account_title">"아래 UTM 속성으로 유입된 사람" 중</div>
                          <div>
                            <div class="select_btn">
                              <div class="select_contents">
                                <ui-select :selectData="this.selectUser" data-key="selectUser" :onClick="selectTarget"></ui-select>
                              </div>
                            </div>
                          </div>
                          <div class="account_date" v-if="subSelect">
                          <ui-select :selectData="this.selectSub" data-key="selectSub" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subInput">
                            <input type="text" v-if="subInput"><span>일</span>
                          </div>
                        </div>
                        <div class="generate_url_list">
                          <form id="google_url_form" class="url_list clearfix" v-on:submit.prevent="addAnalyData">
                            <div class="url_select clearfix">
                              <div class="select_btn">
                                <div class="select_contents">
                                  <ui-select id="utm_key" :selectData="this.select12" data-key="select12" :onClick="selectTarget"></ui-select>
                                </div>
                              </div>
                            </div>
                            <div class="url_input">
                              <input id="utm_name" type="text" value="" placeholder="값 입력 후 엔터를 치면 아래에 입력됩니다.">
                            </div>
                          </form>
                        </div>
                      </div>
                    </div>
                    <div class="analytics_tab_wrap">
                      <div class="analytics_tab_widget clearfix">
                        <ul class="clearfix">
                          <li @click="wTabs(0,'wTab')" v-bind:class="[(wTab.tab1 === true) ? 'active' : '']">source</li>
                          <li @click="wTabs(1,'wTab')" v-bind:class="[(wTab.tab2 === true) ? 'active' : '']">medium</li>
                          <li @click="wTabs(2,'wTab')" v-bind:class="[(wTab.tab3 === true) ? 'active' : '']">campaign</li>
                          <li @click="wTabs(3,'wTab')" v-bind:class="[(wTab.tab4 === true) ? 'active' : '']">team</li>
                          <li @click="wTabs(4,'wTab')" v-bind:class="[(wTab.tab5 === true) ? 'active' : '']">content</li>
                          <li @click="wTabs(5,'wTab')" v-bind:class="[(wTab.tab6 === true) ? 'active' : '']">custom</li>
                        </ul>
                      </div>
                      <div class="analytics_tab_list">
                        <div id="tab_list_1" class="analytics_tab_contents clearfix" v-if="wTab.tab1">
                          <ul>
                            <li v-for="(item,index) in gAddData.utm_source" class="sticker_btn"><span>{{ item.name }}</span><span class="close-btn" @click="deleteAnalyData(item,'utm_source')"><img src="../../assets/images/target/target_list_close.png" alt=""></span></li>
                          </ul>
                          <div class="list_close_btn"><button type="button" @click="deleteAnalyData('all','utm_source')"><img src="../../assets/images/target/target_close_btn.png" alt=""></button></div>
                        </div>
                        <div id="tab_list_2" class="analytics_tab_contents clearfix" v-if="wTab.tab2">
                          <ul>
                            <li v-for="(item,index) in gAddData.utm_medium" class="sticker_btn"><span>{{ item.name }}</span><span class="close-btn" @click="deleteAnalyData(item,'utm_medium')"><img src="../../assets/images/target/target_list_close.png" alt=""></span></li>
                          </ul>
                          <div class="list_close_btn"><button type="button" @click="deleteAnalyData('all','utm_meidum')"><img src="../../assets/images/target/target_close_btn.png" alt=""></button></div>
                        </div>
                        <div id="tab_list_3" class="analytics_tab_contents clearfix" v-if="wTab.tab3">
                          <ul>
                            <li v-for="(item,index) in gAddData.utm_campaign" class="sticker_btn"><span>{{ item.name }}</span><span class="close-btn" @click="deleteAnalyData(item,'utm_campaign')"><img src="../../assets/images/target/target_list_close.png" alt=""></span></li>
                          </ul>
                          <div class="list_close_btn"><button type="button" @click="deleteAnalyData('all','utm_campaign')"><img src="../../assets/images/target/target_close_btn.png" alt=""></button></div>
                        </div>
                        <div id="tab_list_4" class="analytics_tab_contents clearfix" v-if="wTab.tab4">
                          <ul>
                            <li v-for="(item,index) in gAddData.utm_team" class="sticker_btn"><span>{{ item.name }}</span><span class="close-btn" @click="deleteAnalyData(item,'utm_team')"><img src="../../assets/images/target/target_list_close.png" alt=""></span></li>
                          </ul>
                          <div class="list_close_btn"><button type="button" @click="deleteAnalyData('all','utm_team')"><img src="../../assets/images/target/target_close_btn.png" alt=""></button></div>
                        </div>
                        <div id="tab_list_5" class="analytics_tab_contents clearfix" v-if="wTab.tab5">
                          <ul>
                            <li v-for="(item,index) in gAddData.utm_content" class="sticker_btn"><span>{{ item.name }}</span><span class="close-btn" @click="deleteAnalyData(item,'utm_content')"><img src="../../assets/images/target/target_list_close.png" alt=""></span></li>
                          </ul>
                          <div class="list_close_btn"><button type="button" @click="deleteAnalyData('all','content')"><img src="../../assets/images/target/target_close_btn.png" alt=""></button></div>
                        </div>
                        <div id="tab_list_6" class="analytics_tab_contents clearfix" v-if="wTab.tab6">
                          <ul>
                            <li v-for="(item,index) in gAddData.utm_custom" class="sticker_btn"><span>{{ item.name }}</span><span class="close-btn" @click="deleteAnalyData(item,'utm_custom')"><img src="../../assets/images/target/target_list_close.png" alt=""></span></li>
                          </ul>
                          <div class="list_close_btn"><button type="button" @click="deleteAnalyData('all','utm_custom')"><img src="../../assets/images/target/target_close_btn.png" alt=""></button></div>
                        </div>
                      </div>
                    </div>
                    <div class="btn_wrap">
                      <button class="before_btn close_pop" @click="tabMove(0)">취소</button>
                      <button class="next_btn">타겟 만들기</button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 구매 탭 -->
              <div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive6.show">
                <div class="target_contents_inner">
                  <div class="target_thead">
                    <div class="main_title">
                      <div><img src="../../assets/images/target/target_logo_01.png" alt="neo"></div>
                      <div class="title_info">
                        <p>구매</p>
                        <p>타겟의 속성을 정의하세요</p>
                      </div>
                    </div>
                    <div class="use_wrap">
                      <div class="use_select">
                        <div class="contents_title">사용픽셀</div>
                        <ui-select :selectData="this.select13" data-key="select13" :onClick="selectTarget"></ui-select>
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
                  </div>
                  <div class="target_tbody">
                    <div class="target_inner_tbody clearfix">
                      <div class="target_generate">
                        <div class="account_info">
                          <div class="account_title">"구매한 사람" 중</div>
                          <div>
                            <ui-select :selectData="this.selectUser2" data-key="selectUser2" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subInput2">
                          	<input type="text"><span>회</span>
                          </div>
                          <div class="account_date" v-if="subInput3">
                          	<input type="text"><span>원</span>
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
              </div>

              <!-- 장바구니 탭 -->
              <div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive7.show">
                <div class="target_contents_inner">
                  <div class="target_thead">
                    <div class="main_title">
                      <div><img src="../../assets/images/target/target_logo_01.png" alt="neo"></div>
                      <div class="title_info">
                        <p>장바구니</p>
                        <p>타겟의 속성을 정의하세요</p>
                      </div>
                    </div>
                    <div class="use_wrap">
                      <div class="use_select">
                        <div class="contents_title">사용픽셀</div>
                        <ui-select :selectData="this.select15" data-key="select15" :onClick="selectTarget"></ui-select>
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
                  </div>
                  <div class="target_tbody">
                    <div class="target_inner_tbody clearfix">
                      <div class="target_generate">
                        <div class="account_info">
                          <div class="account_title">"장바구니 이용자" 중</div>
                          <div>
                            <ui-select :selectData="this.selectUser" data-key="selectUser" :onClick="selectTarget"></ui-select>
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
              </div>

              <!-- 회원가입 탭 -->
              <div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive8.show">
                <div class="target_contents_inner">
                  <div class="target_thead">
                    <div class="main_title">
                      <div><img src="../../assets/images/target/target_logo_01.png" alt="neo"></div>
                      <div class="title_info">
                        <p>회원가입</p>
                        <p>타겟의 속성을 정의하세요</p>
                      </div>
                    </div>
                    <div class="use_wrap">
                      <div class="use_select">
                        <div class="contents_title">사용픽셀</div>
                        <ui-select :selectData="this.select17" data-key="select17" :onClick="selectTarget"></ui-select>
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
                  </div>
                  <div class="target_tbody">
                    <div class="target_inner_tbody clearfix">
                      <div class="target_generate">
                        <div class="account_info">
                          <div class="account_title">"회원가입한 사람" 중</div>
                          <div>
                            <ui-select :selectData="this.selectUser3" data-key="selectUser3" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subSelect">
                          <ui-select :selectData="this.selectSub" data-key="selectSub" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="account_date" v-if="subInput">
                            <input type="text" v-if="subInput"><span>일</span>
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
              </div>

              <!-- 단계별 전환 -->
              <div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive9.show">
                <div class="target_contents_inner">
                  <div class="target_thead">
                    <div class="main_title">
                      <div><img src="../../assets/images/target/target_logo_08.png" alt="neo"></div>
                      <div class="title_info">
                        <p>단계별 전환</p>
                        <p>타겟의 속성을 정의하세요</p>
                      </div>
                    </div>
                    <div class="use_wrap">
                      <div class="use_select">
                        <div class="contents_title">사용픽셀</div>
                        <ui-select :selectData="this.select19" data-key="select19" :onClick="selectTarget"></ui-select>
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
                  </div>
                  <div class="target_tbody">
                    <div class="target_inner_tbody clearfix">
                      <div class="target_generate">
                        <div class="account_info">
                          <div class="account_title">전환 관련 속성 선택</div>
                          <div>
                            <ui-select :selectData="this.selectUser4" data-key="selectUser4" :onClick="selectTarget"></ui-select>
                          </div>
                          <div class="value_input_wrap" v-if="subInput4">
                            <input type="text">
                            <p>단계 완료 후 이탈 고객</p>
                          </div>
                        </div>
                        <div class="generate_url_list">
                          <div class="url_list clearfix">
                            <div class="url_text clearfix">
                              <p>해당 단계 완료 URL</p>
                            </div>
                            <div class="url_input">
                              <input type="text">
                            </div>
                          </div>
                          <div class="url_list clearfix">
                            <div class="url_text clearfix">
                              <p>다음 단계 완료 URL</p>
                            </div>
                            <div class="url_input">
                              <input type="text">
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="btn_wrap">
                      <button class="before_btn close_pop" @click="tabMove(0)">취소</button>
                      <button class="next_btn">타겟 만들기</button>
                    </div>
                  </div>
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
  mounted() {
    let emptyText = ''
    let textList = []
    let keyList = []

    this.$http.get('/fb_ad_accounts/ad_account_pixels', {
      params: {
        'fb_ad_account_id': localStorage.getItem('fb_ad_account_id')
      }
    })
    .then(res => {
      const response = res.data
      const data = response.data
      const success = response.success
      if (success === 'YES') {
        data.forEach(function(item, index) {
          textList.push(item.name)
          keyList.push(item.id)
          if (index === 0) {
            emptyText = item.name
          }
        })
      } else {
        console.log('/fb_ad_accounts/ad_account_pixels fail')
      }
      return [emptyText, textList, keyList]
    })
    .then(([emptyText, textList, keyList]) => {
      // 픽셀 셀렉트 박스 전체에 세팅 필요
      this.select1.emptyText = emptyText
      this.select1.textList = textList
      this.select1.keyList = keyList
    })
    .catch(err => {
      console.error('/fb_ad_accounts/ad_account_pixels', err)
    })
  },
  data () {
    return {

      subSelect:false,
      subInput:false,
      subInput2:false,
      subInput3:false,
      subInput4:false,

      tabAction:{
        tabActive1:{
          show:true
        },
        tabActive2:{
          show:false
        },
        tabActive3:{
          show:false
        },
        tabActive4:{
          show:false
        },
        tabActive5:{
          show:false
        },
        tabActive6:{
          show:false
        },
        tabActive7:{
          show:false
        },
        tabActive8:{
          show:false
        },
        tabActive9:{
          show:false
        }
      },

      categoryName:'',



      //싱글 셀렉트
      //사이트방문
      select1: {
          emptyText: '전체보기',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },
        //특정페이지
        select3: {
          emptyText: '특정일 동안 미방문 고객',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },
        select5: {
          emptyText: '선택',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },
        //네오
        select6: {
          emptyText: '특정일 동안 미방문 고객',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },
        select9: {
          emptyText: '특정일 동안 미방문 고객',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },
        //구글
        select21: {
          emptyText: '특정일 동안 미방문 고객',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },
        selectUser: {
          emptyText: '전체 고객',
          textList: [
            '전체 고객',
            '이용 시간 상위 고객', // 셀렉트박스 표시 (5/15/25 %)
            '특정일 동안 미방문 고객', // 숫자 입력 텍스트필드 표시
            '구매고객',
            '미 구매고객',
            '장바구니 이용 고객',
            '전환완료 고객',
            '미 전환 고객',
            '회원가입 고객'
          ],
          keyList: [
            'total',
            'usage_time_top', // 셀렉트박스 표시 (5/15/25 %)
            'non_visit', // 숫자 입력 텍스트필드 표시
            'purchase',
            'non_purchase',
            'add_to_cart',
            'conversion',
            'non_conversion',
            'registration'
          ],
        },
        selectUser2: {
          emptyText: '전체 고객',
          textList: [
            '전체 고객',
            '특정 구매횟수 이상 구매 고객', // 셀렉트박스 표시 (5/15/25 %)
            '특정 구매금액 이상 구매 고객', // 숫자 입력 텍스트필드 표시
          ]
        },
        selectUser3: {
          emptyText: '전체 고객',
          textList: [
            '전체 고객',
            '이용 시간 상위 고객', // 셀렉트박스 표시 (5/15/25 %)
            '미 구매 고객',
            '전환 완료 고객',
            '미 전환 고객'
          ]
        },
        selectUser4: {
          emptyText: '미 전환 고객',
          textList: [
            '미 전환 고객',
            '전환 1단계 완료 고객',
            '전환 2단계 완료 고객',
            '전환 3단계 완료 고객',
            '전환 4단계 완료 고객',
            '전환 5단계 완료 고객',
            '특정 단계 완료(URL)'//단계완료 이탈 입력박스
          ]
        },
        selectSub: {
          emptyText: '5%',
          textList: [
            '5%',
            '15%',
            '25%'
          ]
        },
        select12: {
          emptyText: 'utm_source',
          textList: [
            'utm_source',
            'utm_medium',
            'utm_campaign',
            'utm_term',
            'utm_content',
            'utm_custom'
          ]
        },
        //구매
        select13: {
          emptyText: '특정일 동안 미방문 고객',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },
        //장바구니
        select15: {
          emptyText: '특정일 동안 미방문 고객',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },
        //회원가입
        select17: {
          emptyText: '특정일 동안 미방문 고객',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },
        //단계별 전환
        select19: {
          emptyText: '특정일 동안 미방문 고객',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },
        select20: {
          emptyText: '특정일 동안 미방문 고객',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },


        //sample
        advs:[
            { "number": "1", "name": "LF몰", "campaign":"페이스북1", "count":"3,716", "type_id":"13" },
          { "number": "2", "name": "LF몰2", "campaign":"페이스북2", "count":"3,716", "type_id":"11" },
          { "number": "3", "name": "LF몰3", "campaign":"페이스북3", "count":"3,716", "type_id":"15" },
          { "number": "4", "name": "LF몰4", "campaign":"페이스북4", "count":"3,716", "type_id":"17" }
        ],
        addAdvs:[],
        checkData:[],
        selected:[],

        //tabs
        wTab:{
          tab1:true,
          tab2:false,
          tab3:false,
          tab4:false,
          tab5:false,
          tab6:false
        },
        //analytics sample
        gData:{
      utm_source:[
        {
          number:1,
          name:"naver"
        },
        {
          number:2,
          name:"daum"
        },
        {
          number:3,
          name:"google"
        }
      ],
          utm_medium:[],
          utm_compaign:[],
          utm_team:[],
          utm_content:[],
          utm_custom:[],
        },


        //analytics add sample
        gAddData:{
          utm_source:[
            {
              number:1,
              name:"naver"
            },
            {
              number:2,
              name:"daum"
            },
            {
              number:3,
              name:"google"
            }
          ],
          utm_medium:[
            {
              number:1,
              name:"naver"
            },
            {
              number:2,
              name:"daum"
            },
            {
              number:3,
              name:"google"
            }
          ],
          utm_campaign:[
            {
              number:1,
              name:"naver"
            },
            {
              number:2,
              name:"daum"
            },
            {
              number:3,
              name:"google"
            }
          ],
          utm_team:[
            {
              number:1,
              name:"naver"
            },
            {
              number:2,
              name:"daum"
            },
            {
              number:3,
              name:"google"
            }
          ],
          utm_content:[
            {
              number:1,
              name:"naver"
            },
            {
              number:2,
              name:"daum"
            },
            {
              number:3,
              name:"google"
            }
          ],
          utm_custom:[
            {
              number:1,
              name:"naver"
            },
            {
              number:2,
              name:"daum"
            },
            {
              number:3,
              name:"google"
            }
          ]
        },



        fields:[
          //sample
          {
            "number":0,
            "key":0,
            "select":{
              emptyText: 'URL선택',
              textList: [
                '전체URL',
                '부분URL'
              ]
            }
          }
        ],


    }
  },
  methods: {
    //페이지 방문 추가 삭제
    fieldBtn(item,type) {
      let index = 0
      if(type === 'add') {
        index++
        let obj = {
          "number":index,
            "key":index,
            "select":{
              emptyText: 'URL선택',
              textList: [
                '전체URL',
                '부분URL'
              ]
            }
        }
        this.fields.push(obj)
      }else{
        index--
        this.fields.splice(this.fields.indexOf(item), 1)
      }
  },
  //타겟만들기 카테고리 탭
  tabMove(activeNumber, beforeNumber) {
    let tabArray = ['tabActive1','tabActive2','tabActive3','tabActive4','tabActive5','tabActive6','tabActive7','tabActive8','tabActive9']
    let pageNum = (activeNumber == 0) ? '1':'2'

    document.getElementById('page-number').innerText = pageNum

    for(let i = 0; i < tabArray.length; i++) {
      if(i == activeNumber) {
        this.tabAction[tabArray[i]].show = true
      }else{
        this.tabAction[tabArray[i]].show = false
      }
    }
    //리셋 데이터
    //공용 서브 탭 초기화
    this.wTab = {
        tab1:true,
        tab2:false,
        tab3:false,
        tab4:false,
        tab5:false,
        tab6:false
    },
    //서브 셀렉터 초기화
    this.subSelect = false
    this.subInput = false
    this.subInput2 = false
    this.subInput3 = false
  },
  //서브 공용 탭
  wTabs(num,obj) {
    const tabs = Object.keys(this[obj])
    for(let i = 0; i < tabs.length; i++) {
      if(num == i) {
        this.wTab[tabs[i]] = true
      }else{
        this.wTab[tabs[i]] = false
      }
    }
  },
  //개별 셀렉팅
  selectTarget(item) {
    const key = event.target.closest('.select_btn').getAttribute('data-key')
    const textCheck = item.replace(/\s/gi, "")
  	this.subSelect = false
  	this.subInput = false
  	this.subInput2 = false
  	this.subInput3 = false
    this.subInput4 = false
    //서브 입력창 체크
    if(textCheck === '이용시간상위고객') {
    	this.subSelect = true
    }else if(textCheck === '특정일동안미방문고객') {
    	this.subInput = true
    }else if(textCheck === '특정구매횟수이상구매고객') {
     	this.subInput2 = true
    }else if(textCheck === '특정구매금액이상구매고객') {
    	this.subInput3 = true
    }else if(textCheck === '특정단계완료(URL)'){
      this.subInput4 = true
    }
    this[key].emptyText = item
  },
  //멀티 셀렉팅
  multiSelect(item, index) {
    const key = event.target.closest('.select_btn').getAttribute('data-key')
    this.fields[key].select.emptyText = item
  },

  //매체 삭제
  deleteAddAdvs(item) {
    const checkAdd = this.addAdvs
    const addListEl = document.getElementById('adv-list-2')
    const addlistLi = addListEl.getElementsByTagName('li')
    if(item === 'all') {
        for(let i = 0; i < addlistLi.length; i++) {
          this.advs.push(checkAdd[i])
        }
        this.addAdvs.splice(0, addlistLi.length)
    }else{
      this.addAdvs.splice(this.addAdvs.indexOf(item), 1)
      this.advs.push(item)
    }
  },
  //구글애널리틱스 매체 추가
  addAnalyData() {
    const elId = event.target.id
    const utmKey = document.getElementById('utm_key').getElementsByClassName('select')[0].innerText.replace(/\s/gi, "")
    const utmName = document.getElementById('utm_name').value
    const gData = this.gAddData[utmKey]
    const keyData = this.select12.textList
    const newData = {
      number:gData.length + 1,
      name:utmName
    }
    //선택필드 탭 활성화
    for(let i = 0; i < keyData.length; i++) {
      if(keyData[i] === utmKey) {
        this.wTabs(i,'wTab')
        break
      }
    }
    //동일 이름 체크
    for(let i = 0; i < gData.length; i++) {
      if(gData[i].name === utmName) {
        alert('같은 UTM값이 존재합니다.')
        break
        return false
      }
    }
    gData.push(newData)

    return false
  },
  //구글애널리틱스 매체삭제
  deleteAnalyData(item, key){
    const elId = event.target.closest('.analytics_tab_contents').id
    const addListEl = document.getElementById(elId)
    const addlistLi = addListEl.getElementsByTagName('li')

    if(item === 'all') {
      this.gAddData[key].splice(0, addlistLi.length)
    }else{
      this.gAddData[key].splice(this.gAddData[key].indexOf(item), 1)
    }
  },

  //전체선택
  allCheck(value,key1,key2,before,after) {
    const me = this
    var selected = []
        if (value) {
            this.checkFilter(key1)
            me[key1].forEach(function (item) {
                selected.push(item.number)
            });
        }
        me[key2] = selected;
  },
  //체크리스트 추가
  checkList (before,after) {

    const me = this

    this.checkFilter(before)

    me[after] = me[after].concat(me.checkData)
    me.checkData.forEach(function(value, index) {
      me[before] = me[before].filter(function(item) {
        return item !== value
      })
    })

    this.selected = []
    me.checkData = []
  },

  //체크 중복 필터
  checkFilter(type) {
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
  },

  createVisitSite () {
    let params = {
      target_type: 'visit_site',
      pixel_id: '',
      name: '',
      rentention_days: 0,

      detail: '',
      input_percent: 0
    }

    console.log(params)

    // this.$http.post('/pickdata_account_target/custom_target', params)
    // .then((response) => {
    //   var success = response.data.success;
    //   if (success == "YES") {
    //
    //   } else {
    //
    //   }
    //   this.$emit('close')
    // })
    // .catch(err => {
    //   this.$emit('close')
    //   console.log('/pickdata_account_target/custom_target: ', err)
    // })
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
