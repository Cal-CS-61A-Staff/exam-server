import React, { useEffect } from "react";
import { typeset } from "MathJax";
import Question from "./Question";

export default function Exam({ exam }) {
    useEffect(() => typeset(), [exam]);
    return (
        <div className="exam">
            {exam.groups.map((group, i) => <Group group={group} i={i} />)}
        </div>
    );
}

function Group({ group, i }) {
    return (
        <>
            <div>
                <h3 style={{ marginBottom: 0 }}>
                    <b>
                        Q
                        {i + 1}
                    </b>
                    {" "}
                    {group.name}
                </h3>
                <small>
                    Points:
                    {" "}
                    {group.points}
                </small>
                {/* eslint-disable-next-line react/no-danger */}
                <div dangerouslySetInnerHTML={{ __html: group.html }} />
                { group.questions.map((question, j) => (
                    <Question question={question} i={i} j={j} />))}
            </div>
            <hr />
            <br />
        </>
    );
}
