__d(function(g,r,i,a,m,e,d){"use strict";Object.defineProperty(e,'__esModule',{value:!0});var o=r(d[6]).connect(function(o,t){var n=t.modalPostId,l=t.tagName,s=r(d[0]).getViewer(o),u=i(d[1])(o.tags.get(l)),c=u.advisory,w=c&&c.acknowledged||!1,p=r(d[2]).getVisibleRecentMediaByTagName(o,l),v=o.navigation;return{allowFollowing:u.allowFollowing,contentAdvisory:c,contentAdvisoryAcknowledged:w,hasReel:!!o.stories.reels.get(r(d[3]).getReelIdForTag(l)),id:u.id,isFollowing:u.isFollowing,modalPostId:n,nullState:u.nullState,pageViewCount:(null===v||void 0===v?void 0:v.pageViewCount)||1,postCount:u.postCount,posts:p,profilePictureUrl:u.profilePictureUrl,showLoggedOutLoginModal:v.isLoginModalOpen,tagName:l,topPosts:r(d[2]).getAllTopMediaByTagName(o,l),viewer:s,viewportWidth:o.displayProperties.viewportWidth,relatedTags:u.relatedTags}},function(o,t){return{onLoadExtras:function(n){o(r(d[4]).loadTagPageExtras(t.tagName,n))},onPageView:function(t,n,l){o(r(d[5]).incrementNewPageViewCount(t,'hashtag',n,l))},onUnloadTagPage:function(t){o(r(d[4]).unloadTagPage(t))}}})(i(d[7]));e.default=o},16318464,[9699361,9699336,16318465,14090242,13172754,9961881,5,16318466]);
__d(function(g,r,i,a,m,e,d){"use strict";Object.defineProperty(e,'__esModule',{value:!0});var t=(function(t){function o(){for(var o,n=arguments.length,s=new Array(n),l=0;l<n;l++)s[l]=arguments[l];return o=t.call.apply(t,[this].concat(s))||this,o.$TagPage1=r(d[1]).passesServerChecks(r(d[1]).SERVER_CHECK_KEYS.HASHTAG_FOLLOW_ENABLE),o}i(d[0])(o,t);var n=o.prototype;return n.componentDidMount=function(){var t=this.props,o=t.hasReel,n=t.onLoadExtras,s=t.onPageView,l=t.pageViewCount,p=t.tagName,c=t.viewer,h={fetchReel:!!c&&!o,fetchLoggedOutExtras:!c};Object.values(h).some(function(t){return t})&&n(h),s(c,p,l),r(d[1]).isLoggedIn()||i(d[2])._("135","1",{unitId:r(d[3]).getUrlPath(window.location.href)})},n.componentWillUnmount=function(){var t=this.props,o=t.onUnloadTagPage,n=t.tagName,s=t.viewer;r(d[4]).removeContentAdvisory(n,null===s||void 0===s?void 0:s.id),o(n)},n.isSmallScreen=function(){return this.props.viewportWidth<r(d[5]).LANDSCAPE_SMALL_SCREEN_CUTOFF},n.render=function(){var t=null;!0===(this.props.contentAdvisory&&!this.props.contentAdvisoryAcknowledged)||0===this.props.posts.length&&0!==this.props.topPosts.length||null==this.props.postCount||(t=a(d[6]).createElement(i(d[7]),{value:this.props.postCount}));var o=this.isSmallScreen(),n=this.$TagPage1&&(this.props.allowFollowing||!this.props.viewer&&!this.props.contentAdvisory),s=this.props,l=s.contentAdvisoryAcknowledged,p=s.nullState;return a(d[6]).createElement(i(d[8]),{androidAppLink:r(d[9]).buildTagLink(this.props.tagName),iOSAppLink:"tag?name="+this.props.tagName,maxWidth:r(d[5]).SITE_WIDTHS.wide,mobileHeader:a(d[6]).createElement(i(d[10]),{leftActions:a(d[6]).createElement(i(d[11]),null),title:"#"+this.props.tagName}),pageIdentifier:i(d[12]).tagPage},a(d[6]).createElement(i(d[13]),{base:"",id:i(d[12]).tagPage,title:i(d[14])(this.props.tagName)}),null!=p&&l&&a(d[6]).createElement(r(d[15]).Box,{border:!r(d[16]).isMobile(),color:r(d[16]).isMobile()?'ig-secondary-background':'ig-primary-background',marginEnd:r(d[16]).isMobile()?void 0:'auto',marginStart:r(d[16]).isMobile()?void 0:'auto',marginTop:r(d[16]).isMobile()?0:8,width:r(d[16]).isMobile()?void 0:i(d[17])['site-width-wide'].value},a(d[6]).createElement(r(d[15]).StandardMegaphone,{body:p.body,bodyWidth:"auto",color:r(d[16]).isMobile()?'secondary':'primary',title:p.title},a(d[6]).createElement(r(d[15]).MegaphoneAction,{onClick:function(){return r(d[18]).openExternalURL(p.link)},type:p.emphasized?'primary':'secondary'},p.action)),r(d[16]).isMobile()&&a(d[6]).createElement(r(d[15]).Divider,null)),r(d[16]).isMobile()&&!this.props.viewer&&a(d[6]).createElement(i(d[19]),{name:'#'+this.props.tagName}),a(d[6]).createElement(i(d[20]),{hasReel:this.props.hasReel,id:this.props.id,isFollowing:this.props.isFollowing,isFollowingEnable:n,isSmallScreen:o,postCount:t,profilePictureUrl:this.props.profilePictureUrl,relatedTags:this.props.relatedTags,tagName:this.props.tagName}),a(d[6]).createElement(i(d[21]),{tagName:this.props.tagName}),this.props.showLoggedOutLoginModal?a(d[6]).createElement(i(d[22]),{triggeringPageType:"hashtag"}):null)},o})(a(d[6]).Component);e.default=t},16318466,[9699333,9699344,9699356,14090249,16318467,9961680,3,9962156,10092546,9699354,9961872,9961873,9699346,9699345,16318468,9699357,9699341,9764867,9961626,16318469,16318470,16318471,13565957]);
__d(function(g,r,i,a,m,e,d){"use strict";Object.defineProperty(e,'__esModule',{value:!0});var t=function(t){return r(d[0])(2452,{tag_name:t})};e.default=t},16318468,[9699332]);
__d(function(g,r,i,a,m,e,d){"use strict";Object.defineProperty(e,'__esModule',{value:!0}),e.default=function(t){return a(d[0]).createElement(a(d[0]).Fragment,null,a(d[0]).createElement(r(d[1]).Box,{alignContent:"center",color:"ig-primary-background",padding:4},!0===i(d[2])._("132","0")?a(d[0]).createElement(r(d[1]).Text.Headline1,{size:"label",textAlign:"center",weight:"semibold"},t.name):a(d[0]).createElement(r(d[1]).Text.Section,{textAlign:"center"},t.name)),a(d[0]).createElement(r(d[1]).Divider,null))}},16318469,[3,9699357,9699356]);
__d(function(g,r,i,a,m,e,d){"use strict";Object.defineProperty(e,'__esModule',{value:!0}),r(d[0]);var t=(function(t){function n(){return t.apply(this,arguments)||this}i(d[1])(n,t);var l=n.prototype;return l.$TagPageHeader1=function(){return this.props.isFollowingEnable?this.props.isSmallScreen?3:7:0},l.render=function(){var t=this.props,n=t.hasReel,l=t.isFollowingEnable,o=t.isSmallScreen,s=t.postCount,c=t.profilePictureUrl,p=t.relatedTags,E=t.tagName,u=o?77:152,y=r(d[2]).isDesktop()||!l;return a(d[3]).createElement(a(d[3]).Fragment,null,a(d[3]).createElement("header",{className:"id8oV "+(l?"_6pbJJ":"")+" "+(r(d[2]).isDesktop()&&!0===i(d[4])._("67","2")?"L3MTa":"")},a(d[3]).createElement("div",{className:"T7reQ "+(l?"_0FuTv":"")+" "+(n?"pkWJh":"")},a(d[3]).createElement(i(d[5]),{animateOnLoad:!0,entrypoint:"reel_hashtag",size:u,tagName:E},a(d[3]).createElement(i(d[6]),{isLink:!1,profilePictureUrl:c,size:u,tagName:E}))),a(d[3]).createElement("div",{className:"WSpok"},a(d[3]).createElement("div",{className:"f7QXd "+(l?"":"SM9CE")+" "+(l?"HfISj":"")},y&&a(d[3]).createElement(r(d[7]).Box,{marginBottom:3},a(d[3]).createElement(r(d[7]).Text.Headline1,null,"#",E)),a(d[3]).createElement(r(d[7]).Box,{marginBottom:this.$TagPageHeader1()},s),l&&a(d[3]).createElement(i(d[8]),{id:this.props.id,loggingClickPoint:"hashtag_header",loggingContainerModule:"feed_hashtag",tagName:E})),p&&p.length>0&&(r(d[2]).isMobile()?null:a(d[3]).createElement(r(d[7]).Box,{direction:"row",display:"flex",flex:"grow",marginStart:12,marginTop:4,wrap:!0},a(d[3]).createElement(r(d[7]).Text,{breakWord:!0,display:"inline"},a(d[3]).createElement(r(d[7]).Text.Body,{color:"ig-secondary-text",display:"inline"},r(d[9])(1052)),' ',a(d[3]).createElement(r(d[7]).Text.Body,{display:"inline"},p.map(function(t){return a(d[3]).createElement(r(d[7]).Box,{display:"inlineBlock",key:t,paddingY:1,wrap:!0},a(d[3]).createElement(i(d[10]),{className:"LFGs8",tag:t}))}))))))),r(d[2]).isMobile()&&p&&p.length>0&&a(d[3]).createElement(r(d[7]).Box,{direction:"row",display:"flex",flex:"grow",marginBottom:2,marginStart:4,overflow:"scrollX",paddingY:2,wrap:!0},a(d[3]).createElement(r(d[7]).Text,{display:"block",textAlign:"center"},a(d[3]).createElement(r(d[7]).Text.Body,{color:"ig-secondary-text",display:"inline"},r(d[9])(2876)),' ',a(d[3]).createElement(r(d[7]).Text.Body,{display:"inline"},p.map(function(t){return a(d[3]).createElement(r(d[7]).Box,{display:"inlineBlock",key:t,paddingY:1,wrap:!0},a(d[3]).createElement(i(d[10]),{className:"LFGs8",tag:t}))})))))},n})(a(d[3]).Component);e.default=t},16318470,[16318472,9699333,9699341,3,9699356,14090254,9699338,9699357,13172752,9699332,9895972]);
__d(function() {},16318472,[]);
__d(function(g,r,i,a,m,e,d){"use strict";Object.defineProperty(e,'__esModule',{value:!0});var o=(function(o){function t(t){var n;return n=o.call(this,t)||this,n.$TagFollowButton2=function(o){var t=n.props,l=t.id,u=t.isFollowing,s=t.isLoading,c=t.loggingClickPoint,h=t.loggingContainerModule,f=t.tagName;if(t.viewerLoggedIn){if(!s){var w={containerModule:h,clickPoint:c,entityId:l};u?n.props.onUnfollowHashtag(f,w):n.props.onFollowHashtag(f,w)}}else n.props.history.push(n.$TagFollowButton1())},n.state={initialPath:t.history.location.pathname},n}i(d[0])(t,o);var n=t.prototype;return n.$TagFollowButton1=function(){return r(d[1]).buildLoginLink(this.state.initialPath,{source:'followHashtag'})},n.render=function(){var o=this.props,t=o.isFollowing,n=o.isLoading,l=o.viewerLoggedIn;return a(d[2]).createElement(r(d[3]).Button,{color:t?'ig-secondary-button':'ig-primary-button',disabled:n,fullWidth:!0,href:l?void 0:this.$TagFollowButton1(),loading:n,onClick:l?this.$TagFollowButton2:void 0},t&&l?r(d[4]).FOLLOWING_TEXT:r(d[4]).FOLLOW_TEXT)},t})(a(d[2]).Component),t=r(d[7]).withRouter(r(d[8]).connect(function(o,t){var n=r(d[5]).getViewer(o),l=!(!n||!n.id),u=o.tags.get(t.tagName);return{id:null===u||void 0===u?void 0:u.id,isFollowing:null===u||void 0===u?void 0:u.isFollowing,isLoading:null===u||void 0===u?void 0:u.isLoading,viewerLoggedIn:l}},function(o){return{onFollowHashtag:function(t,n){return o(r(d[6]).followHashtag(t,n))},onUnfollowHashtag:function(t,n){return o(r(d[6]).unfollowHashtag(t,n))}}})(o));e.default=t},13172752,[9699333,9699354,3,9699357,9699348,9699361,13172754,6,5]);
__d(function(g,r,i,a,m,e,d){"use strict";Object.defineProperty(e,'__esModule',{value:!0}),r(d[0]);var t=function(t){var o=t.advisory,n=t.onAcknowledge,s=t.onCancel,l=null;o.contents&&(l=o.contents.map(function(t,o){return a(d[1]).createElement("p",{className:"_dyez",key:o},t)}));var p=null,c=o.url;return null!=c&&''!==c&&(p=a(d[1]).createElement("p",{className:"Uff8c"},a(d[1]).createElement(i(d[2]),{href:c},null!=o.url_title&&''!==o.url_title?o.url_title:i(d[3])))),a(d[1]).createElement(i(d[4]),{className:"vEUKb"},a(d[1]).createElement("h2",{className:"Qig5S"},o.title),l,p,a(d[1]).createElement("ul",{className:"IXgqY"},a(d[1]).createElement("li",null,a(d[1]).createElement(r(d[5]).Button,{color:"ig-secondary-button",onClick:n},null!=o.show_posts_button_title&&''!==o.show_posts_button_title?o.show_posts_button_title:r(d[6])(3303))),a(d[1]).createElement("li",null,a(d[1]).createElement(r(d[5]).Button,{color:"ig-secondary-button",onClick:s},r(d[6])(1021)))))},o=(function(o){function n(t){var n;return n=o.call(this,t)||this,n.$TagPageMediaBrowser1=r(d[8]).passesServerChecks(r(d[8]).SERVER_CHECK_KEYS.HASHTAG_FOLLOW_ENABLE),n.$TagPageMediaBrowser2=function(){n.props.onAcknowledgeContentAdvisory(n.getViewerId())},n.$TagPageMediaBrowser3=function(){n.props.history.length>2?n.props.history.goBack():n.props.viewer?n.props.history.replace('/'):r(d[9]).openURL('/')},n.$TagPageMediaBrowser4=function(t){n.state.viewedPosts.has(t.id)||n.setState(function(o){return{postImpressionsCount:o.postImpressionsCount+1,viewedPosts:o.viewedPosts.add(t.id)}}),n.props.onPostImpression(t,n.state.postImpressionsCount,n.props.viewer)},n.$TagPageMediaBrowser5=function(t){n.props.isFetching||n.props.isOldestPostLoaded||t>r(d[10]).PAGE_SIZE&&n.props.onRequestNextPage()},n.state={postImpressionsCount:0,viewedPosts:new Set},n}i(d[7])(n,o);var s=n.prototype;return s.isSmallScreen=function(){return this.props.viewportWidth<r(d[11]).LANDSCAPE_SMALL_SCREEN_CUTOFF},s.getPhotosComponentRenderer=function(){var o=this,n=this.props,s=n.contentAdvisory,l=n.contentAdvisoryAcknowledged;return s&&!l?function(){return a(d[1]).createElement(t,{advisory:s,onAcknowledge:o.$TagPageMediaBrowser2,onCancel:o.$TagPageMediaBrowser3})}:null},s.getViewerId=function(){return this.props.viewer?this.props.viewer.id:null},s.renderTopPostsOnlyExplanation=function(){return a(d[1]).createElement(i(d[4]),{key:"advisory_message"},a(d[1]).createElement("p",{className:"_dyez"},r(d[6])(3262,{hashtag:this.props.tagName,"link that reads learn more":a(d[1]).createElement(r(d[5]).Button,{borderless:!0,href:"https://help.instagram.com/861508690592298",target:"_blank"},i(d[3]))})))},s.renderElectionsIntegrityTopPostsOnlyExplanation=function(){return a(d[1]).createElement(i(d[4]),{key:"advisory_message"},a(d[1]).createElement("p",{className:"_dyez"},r(d[6])(192,{"link that reads learn more":a(d[1]).createElement(r(d[5]).Button,{borderless:!0,href:"https://help.instagram.com/861508690592298",target:"_blank"},i(d[3]))})))},s.renderNoTopPostsExplanation=function(){return a(d[1]).createElement(i(d[4]),{key:"advisory_message"},a(d[1]).createElement("p",{className:"_dyez"},r(d[6])(2185,{hashtag:this.props.tagName,"link that reads learn more":a(d[1]).createElement(r(d[5]).Button,{borderless:!0,href:"https://help.instagram.com/861508690592298",target:"_blank"},i(d[3]))})))},s.render=function(){if(this.props.isInitLoad)return a(d[1]).createElement(r(d[5]).Box,{alignSelf:"center",marginTop:15},a(d[1]).createElement(r(d[5]).Spinner,null));var t=null;!0===(!!this.props.contentAdvisory&&!this.props.contentAdvisoryAcknowledged)||0===this.props.posts.length&&0!==this.props.topPosts.length||null==this.props.postCount||(t=a(d[1]).createElement(i(d[12]),{value:this.props.postCount}));var o=null,n=null,s=this.props.isTopMediaOnly||i(d[13])._("181");s?o=i(d[13])._("181")?this.renderElectionsIntegrityTopPostsOnlyExplanation():this.renderTopPostsOnlyExplanation():null!=this.props.postCount&&this.props.postCount>0&&0===this.props.topPosts.length&&(n=this.renderNoTopPostsExplanation());var l=this.isSmallScreen(),p=this.$TagPageMediaBrowser1&&(this.props.allowFollowing||!this.props.viewer&&!this.props.contentAdvisory);return a(d[1]).createElement(i(d[14]),{analyticsContext:i(d[15]).tagPage,className:"KC1QD",endCursor:this.props.endCursor,isFetching:this.props.isFetching,isOldestPostLoaded:this.props.isOldestPostLoaded,isSmallScreen:l,isTopMediaOnly:s,maxPostsToDisplay:this.props.maxPostsToDisplay,noRecentPostExplanation:o,noTopPostExplanation:n,onImpression:this.$TagPageMediaBrowser4,onIntentClick:this.props.onLoggedOutIntentClickLoginModal,onPostLoadTargetChange:this.$TagPageMediaBrowser5,photoComponentRenderer:this.getPhotosComponentRenderer(),postCount:!p&&t,posts:this.props.posts,scrollLoadingEnabled:this.props.scrollLoadingEnabled,topPosts:this.props.topPosts,viewportWidth:this.props.viewportWidth})},n})(a(d[1]).Component),n=r(d[27]).withRouter(r(d[28]).connect(function(t,o){var n=o.modalPostId,s=o.tagName,l=r(d[16]).getViewer(t),p=i(d[17])(t.tags.get(s)),c=p.advisory,u=Boolean(c&&c.acknowledged),h=r(d[18]).getVisibleRecentMediaByTagName(t,s),P=r(d[18]).getPaginationForTagName(t,s),_=null!=l;return{allowFollowing:p.allowFollowing,contentAdvisory:c,contentAdvisoryAcknowledged:u,id:p.id,isInitLoad:!P&&0===h.length,isFetching:null!=P&&r(d[19]).isFetching(P),isOldestPostLoaded:null!=P&&!r(d[19]).hasNextPage(P),isTopMediaOnly:p.isTopMediaOnly,maxPostsToDisplay:h.length,modalPostId:n,postCount:p.postCount,posts:h,profilePictureUrl:p.profilePictureUrl,scrollLoadingEnabled:!!_||h.length>r(d[10]).PAGE_SIZE,tagName:s,viewer:l,viewportWidth:t.displayProperties.viewportWidth,topPosts:r(d[18]).getAllTopMediaByTagName(t,s)}},function(t,o){var n=o.tagName;return{onRequestNextPage:function(){t(r(d[20]).requestNextTagMedia(n))},onAcknowledgeContentAdvisory:function(o){t(r(d[21]).acknowledgeContentAdvisory(n,o))},onLoggedOutIntentClickLoginModal:function(o,n){var s=r(d[22]).isDesktop()?'feature_wall':'content_wall';t(r(d[23]).openLoginModal(s,o,n))},onPostImpression:function(o,s,l){l||i(d[13])._("91")||r(d[8]).isWhitelistedCrawlBot()||r(d[22]).isDesktop()&&!0===i(d[24])._("45","35")||s>(i(d[13])._("128")?r(d[25]).LOGGED_OUT_JP_POST_IMPRESSION_LIMIT:r(d[25]).LOGGED_OUT_TAG_POST_IMPRESSION_LIMIT)&&t(r(d[23]).openLoginModal('content_wall',r(d[26]).buildTagLink(n),'hashtag_posts_impression_limit'))}}})(o));e.default=n},16318471,[16318473,3,9961552,16318474,16318475,9699357,9699332,9699333,9699344,9961626,16318476,9961680,9962156,9961627,12189708,9699346,9699361,9699336,16318465,9962145,16318477,13172754,9699341,9961881,9699356,14090245,9699354,6,5]);
__d(function() {},16318473,[]);
__d(function(g,r,i,a,m,e,d){"use strict";Object.defineProperty(e,'__esModule',{value:!0});var t=r(d[0])(2417);e.default=t},16318474,[9699332]);
__d(function(g,r,i,a,m,e,d){"use strict";function t(n){return function(u){return u(o.first(n,function(){return u(t(n))}))}}function n(t){return function(u){return u(o.next(t,function(){return u(n(t))}))}}Object.defineProperty(e,'__esModule',{value:!0});var o=r(d[0]).generatePaginationActionCreators({pageSize:r(d[1]).PAGE_SIZE,pagesToPreload:0,getState:function(t,n){return i(d[2])(t.tagMedia.byTagName.get(n)).pagination},queryId:"174a5243287c5f3a7de741089750ab3b",queryParams:function(t){return{tag_name:t}},onUpdate:function(t,n,o){var u,_=[];if(n){var c=i(d[2])(n.hashtag),f=i(d[2])(c.edge_hashtag_to_media||c.edge_hashtag_to_ranked_media);_=(f.edges||[]).map(function(t){return t.node}),u=f.page_info}return{type:r(d[1]).TAG_MEDIA_UPDATED,media:_,pageInfo:u,fetch:t,tagName:o}},onError:function(t,n,o,u){return{type:r(d[1]).TAG_MEDIA_ERRORED,err:t,fetch:n,tagName:o,toast:{text:r(d[3]).FAILED_TO_LOAD_TEXT,actionText:r(d[3]).RETRY_TEXT,actionHandler:u}}}});e.requestTagMedia=t,e.requestNextTagMedia=n,e.updateModalPostId=function(t,n){return{type:r(d[1]).TAG_MEDIA_POST_UPDATED,tagName:t,modalPostId:n}}},16318477,[9962145,16318476,9699336,9699348]);
