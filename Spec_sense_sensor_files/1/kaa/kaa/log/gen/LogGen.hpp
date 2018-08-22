/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


#ifndef KAA_LOG_GEN_LOGGEN_HPP_1210959396__H_
#define KAA_LOG_GEN_LOGGEN_HPP_1210959396__H_


#include "boost/any.hpp"
#include "avro/Specific.hh"
#include "avro/Encoder.hh"
#include "avro/Decoder.hh"

namespace kaa_log {
struct DataCollection_power_frequency_iq_timestamp_adjusted {
    double frequency;
    double power;
    std::vector<uint8_t> iq;
    std::string nodenumber;
    int64_t timestamp;
};

}
namespace avro {
template<> struct codec_traits<kaa_log::DataCollection_power_frequency_iq_timestamp_adjusted> {
    static void encode(Encoder& e, const kaa_log::DataCollection_power_frequency_iq_timestamp_adjusted& v) {
        avro::encode(e, v.frequency);
        avro::encode(e, v.power);
        avro::encode(e, v.iq);
        avro::encode(e, v.nodenumber);
        avro::encode(e, v.timestamp);
    }
    static void decode(Decoder& d, kaa_log::DataCollection_power_frequency_iq_timestamp_adjusted& v) {
        avro::decode(d, v.frequency);
        avro::decode(d, v.power);
        avro::decode(d, v.iq);
        avro::decode(d, v.nodenumber);
        avro::decode(d, v.timestamp);
    }
};

}
#endif
