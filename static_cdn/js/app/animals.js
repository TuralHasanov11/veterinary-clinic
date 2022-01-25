let animalFeedApp = new Vue({
    el: "#animalFeedApp",
    data: {
        feeds:null,
        feedsCount:null,
        nextPage:null,
        prevPage:null,
        selectedFeed:null,
        feed:{
            name:null,
            quantity:null,
            weight:null
        }
    },

    created(){
        this.getFeeds('/animals/feeds/list')
    },

    methods:{
        getFeeds(url){
            fetchData(url)
                .then(data => {
                    this.feeds = data.results
                    this.feedsCount = data.count
                    this.nextPage = data.next
                    this.prevPage = data.previous
                })
                .catch(error => console.error(error));
        },

        createFeed(url=''){

            fetchData(`/animals/feeds/create`, method='POST', this.feed)
                .then(data => {
                    this.feeds.unshift(data)
                })
                .catch(error => console.error(error));
        },

        editFeed(url=''){
            fetchData(`/animals/feeds/${this.selectedFeed.id}/`, method='POST', this.selectedFeed)
                .then(data => {
                    this.feeds.splice(this.feeds.findIndex((el)=>{
                        return el.id == data.feeds.id
                    }), 1, data.feeds)
                   
                })
                .catch(error => console.error(error));
        },

        deleteFeed(url=''){
            fetchData(`/animals/feeds/${this.selectedFeed.id}/delete`, method='POST')
                .then(data => {
                    this.feeds.splice(this.feeds.findIndex((el)=>{
                        return el.id == this.selectedFeed.id
                    }),1);
                })
                .catch(error => console.error(error));
        },

        selectFeed(feed){
            this.selectedFeed = feed
        },

    }
});