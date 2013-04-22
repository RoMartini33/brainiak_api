import unittest

from brainiak.instance.list_resource import Query, merge_by_id


def strip(query_string):
    return [item.strip() for item in query_string.split("\n") if item.strip() != '']


class MergeByIdTestCase(unittest.TestCase):

    def test_no_merge(self):
        values = [
            {
                "@id": 1,
                "some property": "some value",
            },
            {
                "@id": 2,
                "some property": "some other value",
            }
        ]
        computed = merge_by_id(values)
        self.assertEqual(computed, values)

    def test_single_merge(self):
        values = [
            {
                "@id": 1,
                "some property": "some value",
            },
            {
                "@id": 2,
                "some property": "some other value",
            },
            {
                "@id": 1,
                "some property": "a thid value",
            }
        ]
        expected = [
            {
                "@id": 1,
                "some property": ["some value", "a thid value"],
            },
            {
                "@id": 2,
                "some property": "some other value",
            }
        ]
        computed = merge_by_id(values)
        self.assertEqual(computed, expected)

    def test_two_merges(self):
        values = [
            {
                "@id": 1,
                "some property": "some value",
            },
            {
                "@id": 2,
                "some property": "some other value",
            },
            {
                "@id": 1,
                "some property": "a thid value",
            },
            {
                "@id": 2,
                "some property": "last value",
            }
        ]
        expected = [
            {
                "@id": 1,
                "some property": ["some value", "a thid value"]
            },
            {
                "@id": 2,
                "some property": ["some other value", "last value"]
            }
        ]
        computed = merge_by_id(values)
        self.assertEqual(computed, expected)


class ListQueryTestCase(unittest.TestCase):

    default_params = {
            "class_uri": "http://some.graph/SomeClass",
            "lang": "",
            "graph_uri": "http://some.graph/",
            "per_page": "10",
            "page": "0",
            "p": "?predicate",
            "o": "?object",
            "sort_by": "",
            "sort_order": "asc",
            "sort_include_empty": "1"
    }
    maxDiff = None

    def test_query_without_extras(self):
        params = self.default_params
        query = Query(params)
        computed = query.to_string()
        expected = """
        DEFINE input:inference <http://semantica.globo.com/ruleset>
        SELECT DISTINCT ?label, ?subject
        WHERE {
            GRAPH ?g { ?subject a <http://some.graph/SomeClass> ;
                     rdfs:label ?label .
                     }
            FILTER(?g = <http://some.graph/>) .
        }

        LIMIT 10
        OFFSET 0
        """
        self.assertEqual(strip(computed), strip(expected))

    def test_query_with_pagination(self):
        params = self.default_params.copy()
        params["per_page"] = "15"
        params["page"] = "2"
        query = Query(params)
        computed = query.to_string()
        expected = """
        DEFINE input:inference <http://semantica.globo.com/ruleset>
        SELECT DISTINCT ?label, ?subject
        WHERE {
            GRAPH ?g { ?subject a <http://some.graph/SomeClass> ;
                     rdfs:label ?label .
                     }
            FILTER(?g = <http://some.graph/>) .
        }
        LIMIT 15
        OFFSET 30
        """
        self.assertEqual(strip(computed), strip(expected))

    def test_query_with_predicate_as_uri(self):
        params = self.default_params.copy()
        params["p"] = "http://some.graph/predicate"
        query = Query(params)
        computed = query.to_string()
        expected = """
        DEFINE input:inference <http://semantica.globo.com/ruleset>
        SELECT DISTINCT ?label, ?object, ?subject
        WHERE {
            GRAPH ?g { ?subject a <http://some.graph/SomeClass> ;
                     rdfs:label ?label ;
                     <http://some.graph/predicate> ?object .
                     }
            FILTER(?g = <http://some.graph/>) .
        }
        LIMIT 10
        OFFSET 0
        """
        self.assertEqual(strip(computed), strip(expected))

    def test_query_with_predicate_as_rdfs_label(self):
        params = self.default_params.copy()
        params["p"] = "rdfs:label"
        query = Query(params)
        computed = query.to_string()
        expected = """
        DEFINE input:inference <http://semantica.globo.com/ruleset>
        SELECT DISTINCT ?label, ?subject
        WHERE {
            GRAPH ?g { ?subject a <http://some.graph/SomeClass> ;
                     rdfs:label ?label .
                     }
            FILTER(?g = <http://some.graph/>) .
        }
        LIMIT 10
        OFFSET 0
        """
        self.assertEqual(strip(computed), strip(expected))

    def test_query_with_predicate_as_compressed_uri(self):
        params = self.default_params.copy()
        params["p"] = "schema:Creature"
        query = Query(params)
        computed = query.to_string()
        expected = """
        DEFINE input:inference <http://semantica.globo.com/ruleset>
        SELECT DISTINCT ?label, ?object, ?subject
        WHERE {
            GRAPH ?g { ?subject a <http://some.graph/SomeClass> ;
                     rdfs:label ?label ;
                     <http://schema.org/Creature> ?object .
                     }
            FILTER(?g = <http://some.graph/>) .
        }
        LIMIT 10
        OFFSET 0
        """
        self.assertEqual(strip(computed), strip(expected))

    def test_query_with_predicate_and_object_as_literal(self):
        params = self.default_params.copy()
        params["p"] = "schema:Creature"
        params["o"] = "Xubiru"
        query = Query(params)
        computed = query.to_string()
        expected = """
        DEFINE input:inference <http://semantica.globo.com/ruleset>
        SELECT DISTINCT ?label, ?subject
        WHERE {
            GRAPH ?g { ?subject a <http://some.graph/SomeClass> ;
                     rdfs:label ?label ;
                     <http://schema.org/Creature> "Xubiru" .
                     }
            FILTER(?g = <http://some.graph/>) .
        }
        LIMIT 10
        OFFSET 0
        """
        self.assertEqual(strip(computed), strip(expected))

    def test_query_with_predicate_and_object_as_literal_with_lang(self):
        params = self.default_params.copy()
        params["p"] = "schema:Creature"
        params["o"] = "Xubiru"
        params["lang"] = "pt"
        query = Query(params)
        computed = query.to_string()
        expected = """
        DEFINE input:inference <http://semantica.globo.com/ruleset>
        SELECT DISTINCT ?label, ?subject
        WHERE {
            GRAPH ?g { ?subject a <http://some.graph/SomeClass> ;
                     rdfs:label ?label ;
                     <http://schema.org/Creature> "Xubiru"@pt .
                     }
            FILTER(langMatches(lang(?label), "pt") OR langMatches(lang(?label), "")) .
            FILTER(?g = <http://some.graph/>) .
        }
        LIMIT 10
        OFFSET 0
        """
        self.assertEqual(strip(computed), strip(expected))

    def test_query_with_sort_by(self):
        params = self.default_params.copy()
        params["sort_by"] = "dbpedia:predicate"
        params["sort_order"] = "asc"
        query = Query(params)
        computed = query.to_string()
        expected = """
        DEFINE input:inference <http://semantica.globo.com/ruleset>
        SELECT DISTINCT ?label, ?sort_object, ?subject
        WHERE {
            GRAPH ?g { ?subject a <http://some.graph/SomeClass> ;
                     rdfs:label ?label .
            OPTIONAL {?subject <http://dbpedia.org/ontology/predicate> ?sort_object} }
            FILTER(?g = <http://some.graph/>) .
        }
        ORDER BY ASC(?sort_object)
        LIMIT 10
        OFFSET 0
        """
        self.assertEqual(strip(computed), strip(expected))

    def test_query_with_sort_exclude_empty(self):
        params = self.default_params.copy()
        params["sort_by"] = "dbpedia:predicate"
        params["sort_order"] = "asc"
        params["sort_include_empty"] = "0"
        query = Query(params)
        computed = query.to_string()
        expected = """
        DEFINE input:inference <http://semantica.globo.com/ruleset>
        SELECT DISTINCT ?label, ?sort_object, ?subject
        WHERE {
            GRAPH ?g { ?subject a <http://some.graph/SomeClass> ;
                     rdfs:label ?label ;
                     <http://dbpedia.org/ontology/predicate> ?sort_object .
                     }
            FILTER(?g = <http://some.graph/>) .
        }
        ORDER BY ASC(?sort_object)
        LIMIT 10
        OFFSET 0
        """
        self.assertEqual(strip(computed), strip(expected))

    def test_query_with_desc_sort_by_rdfs_label(self):
        params = self.default_params.copy()
        params["sort_by"] = "rdfs:label"
        params["sort_order"] = "desc"
        query = Query(params)
        computed = query.to_string()
        expected = """
        DEFINE input:inference <http://semantica.globo.com/ruleset>
        SELECT DISTINCT ?label, ?subject
        WHERE {
            GRAPH ?g { ?subject a <http://some.graph/SomeClass> ;
                     rdfs:label ?label .
                     }
            FILTER(?g = <http://some.graph/>) .
        }
        ORDER BY DESC(?label)
        LIMIT 10
        OFFSET 0
        """
        self.assertEqual(strip(computed), strip(expected))

    def test_query_with_sort_by_object_of_predicate(self):
        params = self.default_params.copy()
        params["p"] = "schema:another_predicate"
        params["sort_by"] = "schema:another_predicate"
        params["sort_order"] = "desc"
        query = Query(params)
        computed = query.to_string()
        expected = """
        DEFINE input:inference <http://semantica.globo.com/ruleset>
        SELECT DISTINCT ?label, ?object, ?subject
        WHERE {
            GRAPH ?g { ?subject a <http://some.graph/SomeClass> ;
                     rdfs:label ?label ;
                     <http://schema.org/another_predicate> ?object .
                     }
            FILTER(?g = <http://some.graph/>) .
        }
        ORDER BY DESC(?object)
        LIMIT 10
        OFFSET 0
        """
        self.assertEqual(strip(computed), strip(expected))

    def test_count_query_without_extras(self):
        params = self.default_params
        query = Query(params)
        computed = query.to_string(count=True)
        expected = """
        DEFINE input:inference <http://semantica.globo.com/ruleset>
        SELECT count(DISTINCT ?subject) as ?total
        WHERE {
            GRAPH ?g { ?subject a <http://some.graph/SomeClass> ;
                     rdfs:label ?label .
                     }
            FILTER(?g = <http://some.graph/>) .
        }
        """
        self.assertEqual(strip(computed), strip(expected))
