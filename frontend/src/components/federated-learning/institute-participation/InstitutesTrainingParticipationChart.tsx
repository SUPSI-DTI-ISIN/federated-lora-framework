import {Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";
import type {InstituteTrainingParticipationDTO} from "@isin/institute-service-client";
import {InstitutesTrainingParticipationChartCustomTooltip} from "./InstitutesTrainingParticipationChartCustomTooltip.tsx";
import type {BarShapeProps} from "recharts/types/cartesian/Bar";
import {useEffect, useState} from "react";

const getTickColor = () =>
    document.documentElement.getAttribute("data-theme") === "dark" ? "#e2e8f0" : "#1e293b";

const getAxisLineColor = () =>
    document.documentElement.getAttribute("data-theme") === "dark" ? "#334155" : "#cbd5e1";

const useAxisColors = () => {
    const [tickColor, setTickColor] = useState(getTickColor);
    const [lineColor, setLineColor] = useState(getAxisLineColor);
    useEffect(() => {
        const update = () => {
            setTickColor(getTickColor());
            setLineColor(getAxisLineColor());
        };
        const observer = new MutationObserver(update);
        observer.observe(document.documentElement, {attributes: true, attributeFilter: ["data-theme"]});
        return () => observer.disconnect();
    }, []);
    return {tickColor, lineColor};
};

interface InstitutesTrainingParticipationChartProps {
    institutesTrainingParticipation: InstituteTrainingParticipationDTO[];
}

const GRADIENT_REACHABLE = "grad-reachable";
const GRADIENT_UNREACHABLE = "grad-unreachable";

const BarShape = (props: BarShapeProps) => {
    const {x, y, width, height} = props;
    const payload = props.payload as InstituteTrainingParticipationDTO;
    if (!width || width <= 0) return null;

    const r = 6;
    const fill = payload.is_reachable
        ? `url(#${GRADIENT_REACHABLE})`
        : `url(#${GRADIENT_UNREACHABLE})`;

    return (
        <path
            d={`M${x},${y + r} a${r},${r} 0 0 1 ${r},-${r} h${width - r} v${height} h${-(width - r)} a${r},${r} 0 0 1 -${r},-${r} Z`}
            fill={fill}
        />
    );
};

export const InstitutesTrainingParticipationChart = ({institutesTrainingParticipation}: InstitutesTrainingParticipationChartProps) => {
    const {tickColor, lineColor} = useAxisColors();

    const chartData = institutesTrainingParticipation.map((inst) => ({
        ...inst,
        trainable_samples_number: inst.is_reachable ? (inst.trainable_samples_number ?? 0) : 0,
    }));

    return (
        <ResponsiveContainer width="100%" height={Math.max(160, chartData.length * 36)}>
            <BarChart
                data={chartData}
                layout="vertical"
                margin={{top: 4, right: 32, left: 8, bottom: 4}}
            >
                <defs>
                    <linearGradient id={GRADIENT_REACHABLE} x1="0" y1="0" x2="1" y2="0">
                        <stop offset="0%" stopColor="#6366f1" stopOpacity={0.85}/>
                        <stop offset="100%" stopColor="#a78bfa" stopOpacity={1}/>
                    </linearGradient>
                    <linearGradient id={GRADIENT_UNREACHABLE} x1="0" y1="0" x2="1" y2="0">
                        <stop offset="0%" stopColor="#94a3b8" stopOpacity={0.5}/>
                        <stop offset="100%" stopColor="#cbd5e1" stopOpacity={0.7}/>
                    </linearGradient>
                </defs>

                <XAxis
                    type="number"
                    tick={{fontSize: 14, fill: tickColor}}
                    tickLine={{stroke: lineColor}}
                    axisLine={{stroke: lineColor}}
                />
                <YAxis
                    type="category"
                    dataKey="institute_name"
                    tick={{fontSize: 14, fill: tickColor}}
                    tickLine={{stroke: lineColor}}
                    axisLine={{stroke: lineColor}}
                    width={150}
                />
                <Tooltip
                    content={<InstitutesTrainingParticipationChartCustomTooltip/>}
                    cursor={false}
                />
                <Bar
                    dataKey="trainable_samples_number"
                    maxBarSize={22}
                    shape={(props: BarShapeProps) => <BarShape {...props} />}
                />
            </BarChart>
        </ResponsiveContainer>
    );
}
