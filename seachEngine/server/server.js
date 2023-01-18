const { Client } = require('@elastic/elasticsearch');
const client = require('./elasticsearch/client');
const express = require('express');
const cors = require('cors');

const app = express();

app.use(cors());

const filterFields = ["Artists.keyword", "Lyricists.keyword", "Music Composers.keyword", "Genres.keyword", "Metaphors.Source.keyword", "Metaphors.Target.keyword"];

app.get('/filters', (req, res) => {
    const filterFieldResults = {};
    async function sendESRequest() {
        for (let i=0; i < filterFields.length; i++) {
            const body = await client.search({
                index: 'songs',
                body: {
                  size: 0,
                  aggs: {
                      distinct_values: {
                          terms: {
                              field: filterFields[i],
                              size : 100
                          }
                      }
                  }
                },
              });
              filterFieldResults[filterFields[i]] = body.aggregations.distinct_values.buckets;
        }
        res.json(filterFieldResults);
    }
    sendESRequest();
});


app.get('/results', (req, res) => {
    // queryWithFilters = req.params.searchQuery
    // const queryWithFilters = {"search": "ජලය", "matchResults": ["Lyrics", "Lyricists"], "filters": {"Artists.keyword": [],  "Lyricists.keyword": [], "Music Composers.keyword": [], "Genres.keyword":[], "Metaphors.Source.keyword": [], "Metaphors.Target.keyword": []}}
    const queryWithFilters = {"search": "", "matchResults": ["Lyrics", "Lyricists"], "filters": {"Artists.keyword": [],  "Lyricists.keyword": [], "Music Composers.keyword": [], "Genres.keyword":[], "Metaphors.Source.keyword": [], "Metaphors.Target.keyword": []}}

    const filter = [];
    var filterCount = 0;
    matchPhrase = {}
    for (let i=0; i < filterFields.length; i++) {
        for (let j=0; j < queryWithFilters.filters[filterFields[i]].length; j++) {
            matchPhrase = {}
            matchPhrase[filterFields[i]] = queryWithFilters.filters[filterFields[i]][j]
            filter[filterCount] = {
                "match_phrase": matchPhrase
                }
                filterCount++;
        }
    }



    const should = [];
    if (queryWithFilters.search != ""){
        var shouldCount = 0;
        for (let i=0; i < queryWithFilters.matchResults.length; i++) {
            match = {}
            match[queryWithFilters.matchResults[i]] = queryWithFilters.search
            should[shouldCount] = {
                "match": match
                }
                shouldCount++;
    }
    }
      
    const bool = {
        "must": [], 
        "filter": filter,
        "should": should,
        "must_not": []
      };
  
    async function sendESRequest() {
        const body = await client.search({
        index: 'songs',
        body: {
            size: 300,
            query: {
                "bool": bool
            },
        },
        });
        console.log(bool)
        res.json(body.hits.hits);
    }
    sendESRequest();
});

const PORT = process.env.PORT || 3001;

app.listen(PORT, () => console.group(`Server started on ${PORT}`));