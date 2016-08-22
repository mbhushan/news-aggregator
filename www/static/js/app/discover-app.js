/* topojson parser */
L.TopoJSON = L.GeoJSON.extend({
     addData: function(jsonData) {
       if (jsonData.type === "Topology") {
         for (key in jsonData.objects) {
           geojson = topojson.feature(jsonData, jsonData.objects[key]);
           L.GeoJSON.prototype.addData.call(this, geojson);
         }
       }
       else {
         L.GeoJSON.prototype.addData.call(this, jsonData);
       }
     }
   });

function removeHypens(text) {
    if (!text) {
        return text;
    }
    return text.replace(/-/g, ' ');
}

/* skin flipper */
L.Control.SkinChanger = L.Control.extend({
    options: {
        position: 'topleft'
    },

    onAdd: function () {
        var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control skinchanger-control');

        this.weather = L.DomUtil.create('a', 'leaflet-bar-part skinchanger-item skinchanger-weather', container);
        this.weather.href = '#';
        L.DomUtil.create('div', 'glyphicon glyphicon-cloud', this.weather);
        L.DomEvent.on(this.weather, 'click', this._showWeatherClicked, this);
        this.weather.title = 'Show weather';

        this.stories = L.DomUtil.create('a', 'leaflet-bar-part skinchanger-item', container);
        this.stories.href = '#';
        var newsIcon = L.DomUtil.create('img', 'news-icon', this.stories);
        newsIcon.setAttribute('src', '/static/img/news-small.png');

        L.DomEvent.on(this.stories, 'click', this._showNewsClicked, this);
        this.stories.title = 'Show news';

        return container;
    },

    showWeather: function(){},

    _showWeatherClicked: function (e) {
        L.DomEvent.stopPropagation(e);
        L.DomEvent.preventDefault(e);
        this.showWeather();
    },

    showNews: function(){},

    _showNewsClicked: function(e) {
        L.DomEvent.stopPropagation(e);
        L.DomEvent.preventDefault(e);
        this.showNews();
    }
});

var redIcon = L.icon({
    iconUrl: '/static/img/marker-red.png',
    iconSize: [24,24],
    iconAnchor: [12, 23]
});

$(function() {
    var stateFrequency = {"DL": 0, "WB": 30, "HR": 100, "HP": 200, "UP": 500, "JH": 1000, "BR": 0, "JK": 300, "PB": 0, "NL": 0, "PY": 0, "TR": 0, "TN": 0, "RJ": 0, "CH": 0, "AN": 0, "AP": 0, "AS": 0, "AR": 0, "GA": 0, "GJ": 0, "CT": 0, "KA": 0, "ML": 0, "MN": 0, "MH": 0, "KL": 0, "SK": 0, "MP": 0, "UT": 0, "OR": 0, "MZ": 0}

    var mapConfig = {zoomed: false, mapCenter: [23.25, 82.41], defaultZoom: 5, minZoom:4, maxZoom: 7, markers: [], tagMarkers: [],
                    mode: 'news', originalBound: [[37.05, 97.35], [6.74, 68.15]], layerMapping: {}};
    var map = L.map('map', {maxZoom: mapConfig.maxZoom, minZoom: mapConfig.minZoom}).setView(mapConfig.mapCenter, mapConfig.defaultZoom);

    function onMapZoomed(e) {
        if (map.getZoom() >= 6) {
            for (var state in stateToCities.states) {
                var cityNames = stateToCities.states[state];
                for (var i=0; i<cityNames.length; i++) {
                    var marker = L.marker(stateToCities.cities[cityNames[i]].coordinates);
                    marker.addTo(map);
                    marker.name = cityNames[i].toLowerCase();
                    if (stateToCities.cities[cityNames[i]].state) {
                        marker.state = stateToCities.cities[cityNames[i]].state;
                    }
                    marker.on('click', function(e){showSidebarNews(e.target.name, e.target.state)});
                    mapConfig.markers.push(marker);
                }
            }
        } else {
            removeMarkers();
        }
    }

    //map.on('zoomend', onMapZoomed);

    map.fitBounds(mapConfig.originalBound);

    var singleClickTimer = null;

    L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
            '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'examples.map-i875mjb7'
    }).addTo(map);

    $.getJSON('/static/data/india-states.json').done(addTopoData);

    function addTopoData(topoData) {
        topoLayer.addData(topoData);
        topoLayer.addTo(map);
        var layers = topoLayer.getLayers();
        for (var i=0; i<layers.length; i++) {
            mapConfig.layerMapping[layers[i].feature.properties.HASC_1] = {bound: layers[i].getBounds(), name: layers[i].feature.properties.NAME_1};
        }

        setTimeout(function(){
            if (NationStory.userSettings.regionCode) {
                map.fitBounds(mapConfig.layerMapping[NationStory.userSettings.regionCode].bound);
                showSidebarNews(mapConfig.layerMapping[NationStory.userSettings.regionCode].name);
            }
        }, 1000);
    }

    /* map buttons */

    var skinChangerBtns = new L.Control.SkinChanger();
    skinChangerBtns.addTo(map);

    var resetMapBtn = L.easyButton('glyphicon-repeat', resetMap, 'Reset map');
    resetMapBtn.addTo(map);

    skinChangerBtns.showWeather = function() {
        if (mapConfig.mode == 'news') {
            removeTagMarkers();
            resetMap();
            _.each(weatherData, function(city){
                var mapIcon = L.icon({
                    iconUrl: city.icon,
                    iconSize: [50, 50],
                    iconAnchor: [25, 40]
                });

                var marker = L.marker(stateToCities.cities[city.name].coordinates, {icon: mapIcon}).addTo(map);
                marker.name = city.name;
                mapConfig.markers.push(marker);
                marker.on('click', function(e) {
                    var curCity = null;
                    for (var i=0; i<weatherData.length; i++) {
                        if (weatherData[i].name == e.target.name) {
                            curCity = weatherData[i];
                        }
                    }

                    $('.topic').text(curCity.name + ' weather');
                    var str = weatherTemplate({weather: curCity});
                    $('.content').html(str);
                    $('.map-story').show();
                });


            });

            mapConfig.mode = 'weather';
        }
    };

    skinChangerBtns.showNews = function() {
        if (mapConfig.mode == 'weather') {
            removeMarkers();
            mapConfig.mode = 'news';
            showSidebarNews(mapConfig.layerMapping[NationStory.userSettings.regionCode].name);
        }
    }

    // control that shows state info on hover
//     var info = L.control();
//     info.onAdd = function (map) {
//         this._div = L.DomUtil.create('div', 'info');
//         this.update();
//         return this._div;
//     };
//
//     info.update = function (props) {
//         this._div.innerHTML = '<h4>State</h4>' +  (props ?
//             '<b>' + props.NAME_1 + ', ' + props.NAME_0
//             : 'Hover over a state');
//     };
//     info.addTo(map);

    // get color depending on population density value
    function getColor(d) {
        return '#FFEDA0';
    }

    function style(feature) {
        return {
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7,
            fillColor: getColor(stateFrequency[feature.properties.HASC_1])
        };
    }

    function highlightFeature(e) {
        var layer = e.target;

        layer.setStyle({
            weight: 4,
            color: 'white',
            dashArray: '',
            fillOpacity: 0.7,
            fillColor: '#FEB24C'
        });

        if (!L.Browser.ie && !L.Browser.opera) {
            layer.bringToFront();
        }
//         info.update(layer.feature.properties);
    }

    var topoLayer = new L.TopoJSON(null, {
        style: style,
        onEachFeature: onEachFeature});

    function resetHighlight(e) {
        topoLayer.resetStyle(e.target);
        info.update();
    }

    function removeMarkers() {
        var marker = null;
        while(marker = mapConfig.markers.pop()) {
            map.removeLayer(marker);
        }
    }

    function removeTagMarkers() {
        var marker = null;
        while(marker = mapConfig.tagMarkers.pop()) {
            map.removeLayer(marker);
        }
    }

    function zoomToFeature(e) {
//         removeMarkers();

//         if (singleClickTimer) {
//             window.clearTimeout(singleClickTimer);
//             singleClickTimer = null;
//         }

        if (false && mapConfig.zoomed) {
            mapConfig.zoomed = false;
            map.setView(mapConfig.mapCenter, mapConfig.defaultZoom);
        } else {
            mapConfig.zoomed = true;
            map.fitBounds(e.target.getBounds());
            //showCities(e.target.feature.properties.HASC_1);
        }
    }

    function showCities(state) {
        var cityNames = stateToCities.states[state];
        for (var i=0; i<cityNames.length; i++) {
            var marker = L.marker(stateToCities.cities[cityNames[i]].coordinates);
            marker.addTo(map);
            marker.name = cityNames[i].toLowerCase();
            marker.on('click', function(e){showSidebarNews(e.target.name)});
            mapConfig.markers.push(marker);
        }
    }

    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: singleClick,
            //dblclick: zoomToFeature
        });
    }

    function singleClick(e) {
//         if (!singleClickTimer) {
//             singleClickTimer = window.setTimeout(singleClickProcess, 300, e);
//         }
        zoomToFeature(e);
        showSidebarNews(e.target.feature.properties.NAME_1);
    }

    function singleClickProcess(e) {
        singleClickTimer = null;

        var stateName = e.target.feature.properties.NAME_1;
        showSidebarNews(stateName);
    }

    function resetMap() {
        if (mapConfig.mode == 'news') {
            removeTagMarkers();
        }

        mapConfig.zoomed = false;
        map.setView(mapConfig.mapCenter, mapConfig.defaultZoom);
        //map.fitBounds(mapConfig.originalBound);
    }

    /* story sidebar */
    var storiesTemplate = _.template($("#discover-stories").html());
    var weatherTemplate = _.template($("#discover-weather").html());

    function showSidebarNews(topic, subtopic, keepMarkers) {
        $('.map-story').show();

        if (!keepMarkers) {
            removeTagMarkers();
        }

        $('.topic').text(topic);
        if (subtopic) {
            $('.sub-topic').html('See stories from <a href="#">' + subtopic + '</a>');
            $('.sub-topic a').click(function(e) {
                e.preventDefault();
                var subtopic = $('.sub-topic a').text();
                showSidebarNews(subtopic);
            });
        } else {
            $('.sub-topic').text('');
        }
        $('.content').html('<div class="align-center">Fetching stories ..</div>');
        $.ajax({
            url: '/api/tag/' + topic.toLowerCase().replace(' ', '-'),
            method: 'GET',
            data: {source:'discover'},
            success: function(data) {
                if (data.stories.length == 0) {
                    $('.content').html('<div class="align-center">No story found.</div>');
                } else {
                    var str = '';

                    str = storiesTemplate({stories:data.stories});
                    $('.content').html(str);
                    $('.story-tag').click(tagClicked);

                    _.each(data.stories, function(story) {
                        if (story.cities) {
                            showLocationMarkers(story.cities);
                        }
                    });
                }

            },
            error: function() {

            }
        });
    }

    var showLocationMarkers = function(cities) {
        _.each(cities, function(city){

            if (city.location) {
                var marker = L.marker(city.location, {icon: redIcon}).addTo(map);

                marker.name = city.name;
                marker.on('click', function(e) {
                    if ($('.map-story').css('display') == 'none') {
                        showSidebarNews(NationStory.util.toTitleCase(removeHypens(e.target.name)), null, true);
                    } else {
                        var selector = "."+e.target.name;
                        var $element = $("."+e.target.name + ":first");
                        var $container = $('.map-story .content');
                        var offset = $element.offset().top;
                        var divheight = $element.height();

                        if(offset < 0 || offset + divheight > $container.height()){
                           $('.map-story .content').animate({
                            scrollTop: $element.offset().top - 130
                            }, 300);
                        }

                        $(selector).addClass('highlighted story-selected');
                        window.setTimeout(function(){$(selector).removeClass('highlighted');}, 1200);
                    }
                });
                mapConfig.tagMarkers.push(marker);
            }
        });

    };

    var tagClicked = function(e){
        e.preventDefault();
        showSidebarNews(NationStory.util.toTitleCase(removeHypens($(e.currentTarget).attr('data'))));
    };

    $('.map-story .close').click(function() {
        $('.map-story').hide();
    });
});
