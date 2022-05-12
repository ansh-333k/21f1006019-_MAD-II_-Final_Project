Vue.createApp({
	data() {
        return {
            html: 'home',
            new_pass: '',
            cnf_pass: '',
            obj: ''
        }
    },
    methods: {
        ht(h) {
            this.html = h
        },
        m(u, o) {
            if(this.html === 'view_deck') {
                this.html = 'deck'
            }
            if(this.html === 'edit_deck') {
                this.obj = o
                this.html = 'update_deck'
            }
            if(this.html === 'remove_deck') {
                window.location = '/m/admin/deck/remove/' + o
            }
            if(this.html === 'export_deck') {
                window.location = '/m/admin/deck/export/' + o
            }
            if(this.html === 'remove_card') {
                window.location = '/m/admin/' + this.obj + '/remove/'  + o
            }
            if(this.html === 'home') {
                window.location = '/m/' + u + '/data/export/report'
            }
            if(this.html === 'decks') {
                window.location = '/m/' + u + '/' + o + '/play/start'
            }
        }
    },
    watch: {
        new_pass: {
            handler() {
                if((this.$refs.new_pass.value != '') && (this.$refs.cnf_pass.value != '') && (this.$refs.new_pass.value != this.$refs.cnf_pass.value)) {
                    this.$refs.alert.style.display = 'initial'
                    this.$refs.submit.style.display = 'none'
                }
                else {
                    this.$refs.alert.style.display = 'none'
                    this.$refs.submit.style.display = 'initial'
                }
            }
        },
        cnf_pass: {
            handler() {
                if((this.$refs.new_pass.value != '') && (this.$refs.cnf_pass.value != '') && (this.$refs.new_pass.value != this.$refs.cnf_pass.value)) {
                    this.$refs.alert.style.display = 'initial'
                    this.$refs.submit.style.display = 'none'
                }
                else {
                    this.$refs.alert.style.display = 'none'
                    this.$refs.submit.style.display = 'initial'
                }
            }
        }
    }
})
.mount('#app')