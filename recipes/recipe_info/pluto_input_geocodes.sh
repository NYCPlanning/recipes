# # docker run --rm\
# #             -v `pwd`:/home/pts\
# #             -w /home/pts\
# #             sptkl/docker-geosupport:19b bash -c "pip install pandas; python3 geocode.py"

docker run --rm\
            -v `pwd`:/home/pts\
            -w /home/pts\
            sptkl/docker-geosupport:19b2 bash -c "pip install pandas; python3 pluto_geocode.py"

psql $CAPDB -c "
DROP TABLE IF EXISTS pluto_input_geocodes;
CREATE TABLE pluto_input_geocodes (
    borough text,
    block text,
    lot text,
    input_hnum text,
    input_sname text,
    easement text,
    billingbbl text,
    bbl text,
    communitydistrict text,
    censustract2010 text,
    censusblock2010 text,
    communityschooldistrict text,
    citycouncildistrict text,
    zipcode text,
    firecompanynumber text,
    policeprecinct text,
    healthcenterdistrict text,
    healtharea text,
    sanitationdistrict text,
    sanitationcollectionscheduling text,
    boepreferredstreetname text,
    numberofexistingstructures text,
    taxmapnumbersectionandvolume text,
    sanbornmapidentifier text,
    xcoord text,
    ycoord text,
    longitude text,
    latitude text,
    grc text,
    grc2 text, 
    msg text,
    msg2 text
);
"
psql $CAPDB -c "COPY pluto_input_geocodes FROM '`pwd`/geo_result.csv' WITH NULL AS '' DELIMITER ',' CSV HEADER;"

psql $CAPDB -c "
ALTER TABLE pluto_input_geocodes
    ADD wkb_geometry geometry(Geometry,4326);

UPDATE pluto_input_geocodes
SET wkb_geometry = ST_SetSRID(ST_Point(longitude::DOUBLE PRECISION,
                    latitude::DOUBLE PRECISION), 4326),
    xcoord = ST_X(ST_TRANSFORM(wkb_geometry, 2263)),
    ycoord = ST_Y(ST_TRANSFORM(wkb_geometry, 2263))
;"


