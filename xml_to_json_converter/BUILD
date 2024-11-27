#py_library(
#    name = "xml_to_json_converter",
#    srcs = ["xml_to_json_converter.py"],
#    deps = [],
#)
#
#genrule(
#    name = "convert_test_output",
#    srcs = [
#        ":test_flaky",
#        ":test_reference",
#        ":xml_to_json_converter",  # Assuming the script is at the root of the workspace
#    ],
#    outs = ["test-output.json"],
#    cmd = "( " +
#          "bazel test //... && " +  # Run all tests
#          "python $(location //xml_to_json_converter:xml_to_json_converter) $(location :test_flaky) $(location :test_reference) > $@" +
#          " )",
#)
