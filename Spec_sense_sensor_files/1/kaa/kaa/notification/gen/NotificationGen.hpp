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


#ifndef KAA_NOTIFICATION_GEN_NOTIFICATIONGEN_HPP_1210959396__H_
#define KAA_NOTIFICATION_GEN_NOTIFICATIONGEN_HPP_1210959396__H_


#include "boost/any.hpp"
#include "avro/Specific.hh"
#include "avro/Encoder.hh"
#include "avro/Decoder.hh"

namespace kaa_notification {
enum power_iq_change_choice {
    Y_change,
    N_change,
};

struct ConfigurationChanges {
    power_iq_change_choice power_iq_change;
    std::string NewSamplingFrequency;
    std::string NewNumberOFBins;
    std::string NewNoAvgdSpectra;
};

}
namespace avro {
template<> struct codec_traits<kaa_notification::power_iq_change_choice> {
    static void encode(Encoder& e, kaa_notification::power_iq_change_choice v) {
        e.encodeEnum(v);
    }
    static void decode(Decoder& d, kaa_notification::power_iq_change_choice& v) {
        v = static_cast<kaa_notification::power_iq_change_choice>(d.decodeEnum());
    }
};

template<> struct codec_traits<kaa_notification::ConfigurationChanges> {
    static void encode(Encoder& e, const kaa_notification::ConfigurationChanges& v) {
        avro::encode(e, v.power_iq_change);
        avro::encode(e, v.NewSamplingFrequency);
        avro::encode(e, v.NewNumberOFBins);
        avro::encode(e, v.NewNoAvgdSpectra);
    }
    static void decode(Decoder& d, kaa_notification::ConfigurationChanges& v) {
        avro::decode(d, v.power_iq_change);
        avro::decode(d, v.NewSamplingFrequency);
        avro::decode(d, v.NewNumberOFBins);
        avro::decode(d, v.NewNoAvgdSpectra);
    }
};

}
#endif
