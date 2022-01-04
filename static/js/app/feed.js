// Feeds

let feedsApp = new Vue({
    el: "#feedsApp",

    data: {
        url:'/animals/feeds/list?page=1',

        feeds:null,
        feedsCount:null,
        
        nextPage:null,
        prevPage:null,
        currentPage:null,
        currentPageNum:null,
        totalPages:null,
        firstPage:null,
        lastPage:null,
        pagination:null,

        loading:false,

        selectedFeed:null,
        feed:{
            name:null,
            quantity:null,
            weight:null,
        },

        searchQuery:null,
        orderByColumn:'name',

        success:false,
        error:false,
        successMessage:null,
        errorMessage:null,
        validationErrors:{},
    },

    created(){
        this.getFeeds(`${this.url}&ordering=${this.orderByColumn}`)
    },

    methods:{
        getFeeds(url){
            this.loading=true
            
            fetchData(url)
                .then(data => {
                    this.feeds = data.results
                    this.feedsCount = data.count
                    this.nextPage = data.links.next
                    this.prevPage = data.links.previous
                    this.currentPageNum = data.current_page
                    this.totalPages = data.total_pages
                    this.firstPage = data.links.first
                    this.lastPage = data.links.last
                    this.currentPage = data.links.current
                    
                    this.loading=false
                    
                })
                .catch(err => {
                    this.handleError(err)
                });
        },


        createFeed(url=''){
            this.loading=true

            fetchData(`/animals/feeds/create`, method='POST', this.feed)
                .then(data => {
                    
                    this.feeds.unshift(data.feed)

                    this.handleSuccess(data)
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        editFeed(url=''){
            this.loading=true

            fetchData(`/animals/feeds/${this.selectedFeed.id}`, method='POST', this.selectedFeed)
                .then(data => {
                    this.feeds.splice(this.feeds.findIndex((el)=>{
                        return el.id == data.feed.id
                    }), 1, data.feed)

                    this.handleSuccess(data)
                   
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        deleteFeed(url=''){
            this.loading=true

            fetchData(`/animals/feeds/${this.selectedFeed.id}/delete`, method='POST')
                .then(data => {
                    this.feeds.splice(this.feeds.findIndex((el)=>{
                        return el.id == this.selectedFeed.id
                    }),1)

                    this.handleSuccess(data)
                })
                .catch(err => {
                    this.handleError(err)
                })
        },


        filtering(column=this.orderByColumn){
            this.orderByColumn = column
            let url = this.url
            
            if(this.orderDirection){
                this.orderDirection=0
            }else{
                this.orderDirection=1
            }

            if(this.searchQuery){
                url+=`&search=${this.searchQuery}`
            }

            if(this.orderDirection){
                url+=`&ordering=${''?this.orderDirection:'-'}${this.orderByColumn}`
            }

            this.getFeeds(url)
        },

        selectFeed(feed){
            this.reset()
            this.clearMessages()
            this.selectedFeed = feed
        },

        clearMessages(){
            this.success=false
            this.error=false
            this.errorMessage=null
            this.successMessage=null
        },

        handleSuccess(data){
            this.reset()
            this.clearMessages()
            this.loading=false
            this.success = true
            this.successMessage = data.message
        },

        handleError(data){
            this.clearMessages()
            this.loading=false

            data=JSON.parse(data.message)
            if(data.message){
                this.reset()
                this.error = true
                this.errorMessage = data.message
            }else{
                this.validationErrors = data
            }
        },

        reset(){
            this.selectedFeed=null
            this.validationErrors={}
            document.querySelector('.btn-close').click();
        }
    }
});




