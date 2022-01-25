// Feeds

let feedsApp = new Vue({
    el: "#feedsApp",

    data: {
        url:'/animals/feeds/list?page=1',

        feeds:[],
        feedsCount:null,
        
        perPage:null,
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
        orderDirection:1,

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
                    this.perPage= data.per_page
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


        filtering(){
            let url = this.url

            if(this.searchQuery){
                url+=`&search=${this.searchQuery}`
            }

            if(this.orderByColumn){
                if(this.orderDirection){
                    url+=`&ordering=${this.orderByColumn}`
                }else{
                    url+=`&ordering=-${this.orderByColumn}`
                }
            }

            this.getFeeds(url)
        },

        orderBy(column='name'){
            
            
            if(column == this.orderByColumn){
                this.orderDirection=Number(!this.orderDirection)
            }else{
                this.orderDirection = 1
                
            }

            this.orderByColumn = column

            this.filtering()

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
            document.querySelectorAll('.btn-close').forEach((el)=>{
                el.click()
            });
        }
    }
});




